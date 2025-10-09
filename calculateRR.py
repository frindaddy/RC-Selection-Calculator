import argparse
from componentLib import E12, E24, E96, E192, buildResistorValueList
import numpy as np
from quantiphy import Quantity

def findBestResistorRatio(rValues: list[float], targetRatio: float, top: int = 1) -> list[float]:
    """Finds the best R1/R2 combinations to achieve a target ratio and displays the top results.

    Args:
        rValues (list[float]): List of resistor values.
        targetRatio (float): Target ratio (R1 / R2).
        top (int, optional): Number of top results to return. Defaults to 1.

    Returns:
        list[dict]: List of dictionaries containing the best R1, R2, Ratio, Error, and Percent Error values.
    """
    ratio = np.array([[r1 / r2 for r2 in rValues] for r1 in rValues])
    error = np.abs(ratio - targetRatio)
    flatIDXSorted = np.argsort(error, axis=None)
    iSorted, jSorted = np.unravel_index(flatIDXSorted, error.shape)

    results = []
    for k in range(min(top, flatIDXSorted.size)):
        i, j = int(iSorted[k]), int(jSorted[k])
        results.append(
            {
                "R1": str(Quantity(rValues[i], "Ω")),
                "R2": str(Quantity(rValues[j], "Ω")),
                "Ratio": str(Quantity(ratio[i, j], "")),
                "Error": str(Quantity(error[i, j], "")),
                "Percent Error": float((error[i, j] / targetRatio) * 100),
            }
        )

    title = f"Top {top} results for target Ratio = {targetRatio:.4f}"
    print(title.center(70))
    print(f"{'R1':>10} {'R2':>10} {'Ratio':>15} {'Error':>15} {'% Error':>10}")
    print("-" * 70)
    for result in results:
        print(f"{result['R1']:>10} {result['R2']:>10} {result['Ratio']:>15} {result['Error']:>15} {result['Percent Error']:>10.4f}")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the best resistor combinations to achieve a target resistor ratio.")
    parser.add_argument("ratio", type=float, help="Target resistor ratio (e.g. 2.1, 0.5, 0.25)")
    parser.add_argument("-r", "--resistor-tolerance", type=float, choices=[0.1, 0.25, 0.5, 1, 2, 5, 10], default=1, help="Resistor tolerance in percent (default: 1%%)")
    parser.add_argument("-n", "--num-results", type=int, default=5, help="Number of top results to display (default: 5)")
    args = parser.parse_args()

    findBestResistorRatio(
        buildResistorValueList(E192 if args.resistor_tolerance <= 0.5 else E96 if args.resistor_tolerance == 1 else E24 if args.resistor_tolerance <= 5 else E12),
        args.ratio,
        top=args.num_results
    )