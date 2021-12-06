import pandas as pd # type: ignore[import]
import numpy as np # type: ignore[import]
from tqdm import tqdm # type: ignore[import]
from pandas import read_excel
from numpy import array
from typing import List, Any, Tuple, Optional
from os import path

class SMP:
    def __init__(
        self,
        fileName: str = "Bảng dự kiến chào giá T9.xlsx",
        sheetName: List[str] = ['29-09'],
        index: int = 0,
        A: List[str] = ['0', '13'],
        n: int = 2,
        priceContract: float = 917.220,
        expectedPrice: List[float] = [0.0]) -> None:
        root_directory = path.dirname(path.dirname(__file__))
        fileName = path.join(root_directory, "../data", fileName)
        df = read_excel(
            fileName,
            sheet_name = sheetName,
            skiprows = 3,
            nrows = 48,
            usecols = "A:J",
            engine="openpyxl"
        )
        self.data = df[sheetName[index]]
        self.A = A
        self.n = n
        self.priceContract = priceContract
        self.expectedPrice = expectedPrice
        
    def strings(self) -> Any:
        index_of = {x: i for i, x in enumerate(self.A)}
        s = [self.A[0]] * self.n
        while True:
            yield ','.join(s)
            for i in range(1, self.n + 1):
                if s[-i] == self.A[-1]:
                    s[-i] = self.A[0]
                else:
                    s[-i] = self.A[index_of[s[-i]] + 1]
                    break
            else:
                break
                
    def revenue(
        self,
        outputContract: Any,
        priceContract: float,
        expectedPrice: Any,
        expectedOutput: Any,
        priceCan: Any
    ) -> Tuple[float, float]:
        expectedRevenue = outputContract*(priceContract - expectedPrice - priceCan) + expectedOutput*(expectedPrice + priceCan)
        expectedRevenueContract = expectedOutput*priceContract
        if expectedRevenueContract.sum():
            result = expectedRevenue.sum() / expectedRevenueContract.sum() * 100 - 100
        else:
            result = -100.0
        return (expectedRevenueContract.sum(), result)
    
    @property
    def scores(self) -> List[Any]:
        configs = self.strings()
        return sorted((
            self.revenue(
                outputContract = self.data['Sản lượng hợp đồng (Qc)'].values,
                priceContract = self.priceContract,
                expectedPrice = array(self.expectedPrice),
                expectedOutput = array([float(e) for e in row.split(',') for _ in (0, 1)]),
                priceCan = self.data['Giá CAN'].values
            ),
            index
        )
            for index, row in enumerate(tqdm(configs, total=pow(2, self.n)))
        )
    
    
    def get_index(self, key: int) -> Optional[List[Any]]:
        configs = self.strings()
        for index, row in enumerate(configs):
            if key == index:
                return [float(e) for e in row.split(',') for _ in (0, 1)]
        return None
    
# predictions = [ 906.3279 ,  925.6272 ,  860.7097 ,  895.0275 ,  879.58545,
#                 874.5338 ,  834.6106 ,  873.2427 ,  852.2836 ,  881.6196 ,
#                 891.3671 ,  873.38794,  865.9101 ,  878.7915 ,  861.1952 ,
#                 866.4713 ,  872.48615,  818.26025,  793.2189 ,  831.8674 ,
#                 807.9853 ,  764.49414,  787.8861 ,  786.6124 ,  775.5425 ,
#                 814.0161 ,  804.66   ,  814.69556,  826.6653 ,  796.9551 ,
#                 862.7443 ,  944.4846 ,  896.7454 , 1000.2273 , 1205.911  ,
#                1325.4023 , 1300.7592 , 1351.2395 , 1344.3483 , 1286.0173 ,
#                1198.8488 , 1407.6852 , 1394.9956 , 1355.9686 , 1217.0107 ,
#                1069.923  , 1072.1171 ,  950.6141 ]
# smp = SMP(expectedPrice = predictions, sheetName = ['29-09'], n = 24)
# # smp = Smp_result(expectedPrice = predictions, sheetName = ['29-09'], A = ['0', '13'], n=24)
# print(smp.get_index(66047))
# scores = smp.scores
# scores_100 = scores[-100:]
# scores_100.sort(key=lambda tup: tup[0][1]) # type: ignore[no-any-return]
# print(scores_100[-3:])