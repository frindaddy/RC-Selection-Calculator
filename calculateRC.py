import argparse
from componentLib import E12, E24, E96, E192, buildResistorValueList, buildCapacitorValueList
import numpy as np
from quantiphy import Quantity

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
    parser.add_argument("tau", type=str, help="Target RC time constant (e.g. 10ms, 0.5s)")
    parser.add_argument("-r", "--resistor-tolerance", type=float, choices=[0.1, 0.25, 0.5, 1, 2, 5, 10], default=1, help="Resistor tolerance in percent (default: 1%%)")
    parser.add_argument("-n", "--num-results", type=int, default=5, help="Number of top results to display (default: 5)")
    args = parser.parse_args()
    
    findBestRC(
        buildResistorValueList(E192 if args.resistor_tolerance <= 0.5 else E96 if args.resistor_tolerance == 1 else E24 if args.resistor_tolerance <= 5 else E12),
        buildCapacitorValueList(E24),
        Quantity(args.tau, 's'),
        top=args.num_results
    )
