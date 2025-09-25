import numpy as np
from quantiphy import Quantity
from decadeTables import E192, E24

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

findBestRC(buildResistorValueList(E192), buildCapacitorValueList(E24), 0.02, top=5)
