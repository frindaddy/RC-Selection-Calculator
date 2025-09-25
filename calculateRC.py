import argparse
import numpy as np
from quantiphy import Quantity

"""Standard electronic decade value tables.
E192 is used for 0.1%, 0.25%, and 0.5% tolerance.
E96 is used for 1% tolerance.
E24 is used for 2% and 5% tolerance.
E12 is used for 10% tolerance.
"""
E192 = [100, 101, 102, 104, 105, 106, 107, 109, 110, 111, 113, 114, 115, 116, 117, 118, 120, 121, 123, 124,
        126, 127, 129, 130, 132, 133, 135, 137, 138, 140, 142, 143, 145, 147, 149, 150, 152, 154, 156, 158, 
        160, 162, 164, 165, 167, 169, 172, 174, 176, 178, 180, 182, 184, 187, 189, 191, 193, 196, 198, 200,
        203, 205, 208, 210, 213, 215, 218, 221, 223, 226, 229, 232, 234, 237, 240, 243, 246, 249, 252, 255,
        258, 261, 264, 267, 271, 274, 277, 280, 284, 287, 291, 294, 298, 301, 305, 309, 312, 316, 320, 324,
        328, 332, 336, 340, 344, 348, 352, 357, 361, 365, 370, 374, 379, 383, 388, 392, 397, 402, 407, 412,
        417, 422, 427, 432, 437, 442, 448, 453, 459, 464, 470, 475, 481, 487, 493, 499, 505, 511, 517, 523,
        530, 536, 542, 549, 556, 562, 569, 576, 583, 590, 597, 604, 612, 619, 626, 634, 642, 649, 657, 665,
        673, 681, 690, 698, 706, 715, 723, 732, 741, 750, 759, 768, 777, 787, 796, 806, 816, 825, 835, 845,
        856, 866, 876, 887, 898, 909, 920, 931, 942, 953, 965, 976, 988 ]

E96 = [ 100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158,
        162, 165, 169, 174, 178, 182, 187, 191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249, 255,
        261, 267, 274, 280, 287, 294, 301, 309, 316, 324, 332, 340, 348, 357, 365, 374, 383, 392, 402, 412,
        422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681,
        698, 715, 732, 750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976 ]

E24 = [ 10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91 ]

E12 = [ 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82 ]

def buildResistorValueList(decadeTable: list[float]) -> list[float]:
    """Builds a list of resistor values based on a given decade table.

    Args:
        decadeTable (list[float]): List of base resistor values for a decade.

    Returns:
        list[list[float]]: List of resistor values across multiple decades.
    """
    multipliers = [0.01, 0.1, 1, 10, 100, 1000, 10000, 100000, 1000000] #[1, 10, 100, 1k, 10k, 100k, 1M, 10M, 100M]
    resistorValueList = []
    
    for multiplier in multipliers:
        for value in decadeTable:
            resistorValueList.append(round(value * multiplier, 2))
    
    return resistorValueList

def buildCapacitorValueList(decadeTable: list[float]) -> list[float]:
    """Builds a list of capacitor values based on a given decade table.

    Args:
        decadeTable (list[float]): List of base capacitor values for a decade.

    Returns:
        list[list[float]]: List of capacitor values across multiple decades.
    """
    multipliers = [0.1e-12, 1e-12, 10e-12, 100e-12] #[1pF, 10pF, 100pF, 1nF]
    addidtionalCapacitorValues = [100e-9, 150e-9, 220e-9, 330e-9, 470e-9, 680e-9,
                                  1e-6, 1.5e-6, 2.2e-6, 3.3e-6, 4.7e-6, 6.8e-6,
                                  10e-6, 15e-6, 22e-6, 33e-6, 47e-6, 68e-6,
                                  100e-6, 150e-6, 220e-6, 330e-6, 470e-6, 680e-6] #[100nF to 680uF]
    capacitorValueList = []
    
    for multiplier in multipliers:
        for value in decadeTable:
            capacitorValueList.append(round(value * multiplier, 15))
    
    capacitorValueList.extend(addidtionalCapacitorValues)
    
    return capacitorValueList

def findBestRC(rValues: list[float], cValues: list[float], targetTau: float, top: int = 1) -> list[float]:
    """Finds the best R and C combinations to achieve a target RC time constant and displays the top results.

    Args:
        rValues (list[float]): List of resistor values.
        cValues (list[float]): List of capacitor values.
        targetTau (float): Target RC time constant.
        top (int, optional): Number of top results to return. Defaults to 1.

    Returns:
        list[dict]: List of dictionaries containing the best R, C, Tau, Error, and Percent Error values.
    """
    tau = np.array([[r * c for c in cValues] for r in rValues])
    error = np.abs(tau - targetTau)
    flatIDXSorted = np.argsort(error, axis=None)
    iSorted, jSorted = np.unravel_index(flatIDXSorted, error.shape)

    results = []
    for k in range(min(top, flatIDXSorted.size)):
        i, j = int(iSorted[k]), int(jSorted[k])
        results.append(
            {
                "R": str(Quantity(rValues[i], "Ω")),
                "C": str(Quantity(cValues[j], "F")),
                "Tau": str(Quantity(tau[i, j], "s")),
                "Error": str(Quantity(error[i, j], "s")),
                "Percent Error": float((error[i, j] / targetTau) * 100),
            }
        )

    title = f"Top {top} results for target Tau = {Quantity(targetTau, 's')}"
    print(title.center(70))
    print(f"{'R':>10} {'C':>10} {'Tau':>15} {'Error':>15} {'% Error':>10}")
    print("-" * 70)
    for result in results:
        print(f"{result['R']:>10} {result['C']:>10} {result['Tau']:>15} {result['Error']:>15} {result['Percent Error']:>10.4f}")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the best resistance and capacitance combinations to achieve a target RC time constant.")
    parser.add_argument("tau", type=str, help="Target RC time constant (e.g., 10ms, 0.5s)")
    parser.add_argument("-r", "--resistor-tolerance", type=float, choices=[0.1, 0.25, 0.5, 1, 2, 5, 10], default=1, help="Resistor tolerance in percent (default: 1%%)")
    parser.add_argument("-n", "--num-results", type=int, default=5, help="Number of top results to display (default: 5)")
    args = parser.parse_args()
    
    findBestRC(
        buildResistorValueList(E192 if args.resistor_tolerance <= 0.5 else E96 if args.resistor_tolerance == 1 else E24 if args.resistor_tolerance <= 5 else E12),
        buildCapacitorValueList(E24),
        Quantity(args.tau, 's'),
        top=args.num_results
    )
