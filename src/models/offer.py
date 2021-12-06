import pandas as pd # type: ignore[import]
import openpyxl # type: ignore[import]
import src.excel as excel
from typing import List
from os import path
import matplotlib.pyplot as plt # type: ignore[import]
import math

class Offer:
    def __init__(
        self,
        Pmin: float = 11.0,
        CSCB: float = 13.0,
        smp: List[float] = [0.0],
        power: List[float] = [0.0],
        mucGiaTran: float = 1503.5
    ) -> None:
        self.column_Pmin = [[Pmin] if elem != 0 else [0] for elem in power]
        self.column_CSCB = [[CSCB] if elem != 0 else [0] for elem in power]
        
        # Từ mức công suất công bố ta ra được các mức công suất trong bản chào
        if CSCB >= 20:
            cacMucCongSuat = [11.0, 14.0, 17.0]
            cacMucCongSuat.append(CSCB)
        elif CSCB >= 17:
            cacMucCongSuat = [11.0, 14.0]
            cacMucCongSuat.append(CSCB)
        elif CSCB >= 14:
            cacMucCongSuat = [11.0]
            cacMucCongSuat.append(CSCB)
        elif CSCB >= 11:
            cacMucCongSuat = [CSCB]
        
        self.cacMucCongSuat = cacMucCongSuat
        self.power = power
        
        # Từ giá biên tham chiếu cho bản chào dự kiến
        # ta ra được 10 mức giá tương ứng với các mức công suất
        z = plt.hist(smp, bins = 10)
        giachao_1 = []
        for elem in z[0]:
            if (elem/48)*10 % 1 >= 0.5:
                giachao_1.append(math.ceil((elem/48)*10))
            else:
                giachao_1.append(math.floor((elem/48)*10))
                
        giachao_2 = []
        for i in range(10):
            if i + 1 <= 10:
                giachao_2.append((z[1][i] + z[1][i+1])/2)
        
        for i, elem in enumerate(giachao_1):
            if elem == 0:
                giachao_2[i] = 0
                
        giachao_1 = [elem for elem in giachao_1 if elem != 0]
        giachao_2 = [elem for elem in giachao_2 if elem != 0]
        giachao = [elem for i, elem in enumerate(giachao_2) for _ in [i for i in range(giachao_1[i])]]
        
        
        # smp.sort()
        # giachao = smp[-5:]
        # giachao = [i for i in giachao for _ in (0, 1)]
        giachao[0] = 0
        giachao[-1] = mucGiaTran
        giachao = [round(elem, 2) for elem in giachao]
        self.giachao = [giachao]
        
    def createOffer(
        self,
        nameExcel: str = 'Bảng chào giá',
        date: str = '29/09/2021'
    ) -> None:
        root_directory = path.dirname(path.dirname(__file__))
        excel_path_in = path.join(root_directory, "../data", "banchao.xlsx")
        excel_path_out = path.join(root_directory, "../data", f"{nameExcel}.xlsx")
        book = openpyxl.load_workbook(excel_path_in, data_only=True)
        sheet = book['Sheet2']
        # Write Pmin, CSCB
        excel.write(sheet, self.column_Pmin, "B5")
        excel.write(sheet, self.column_CSCB, "C5")
        if len(self.cacMucCongSuat) == 1:
            excel.write(sheet, self.column_CSCB, "D5")
            excel.write(sheet, self.column_CSCB, "E5")
            excel.write(sheet, self.column_CSCB, "F5")
            excel.write(sheet, self.column_CSCB, "G5")
            excel.write(sheet, self.column_CSCB, "H5")
            excel.write(sheet, self.column_CSCB, "I5")
            excel.write(sheet, self.column_CSCB, "J5")
            excel.write(sheet, self.column_CSCB, "K5")
            excel.write(sheet, self.column_CSCB, "L5")
            excel.write(sheet, self.column_CSCB, "M5")
        elif len(self.cacMucCongSuat) == 2:
            # [[Pmin] if elem != 0 else [0] for elem in power]
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "D5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "E5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "F5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "G5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "H5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "I5")
            excel.write(sheet, [[self.cacMucCongSuat[1]] if elem != 0 else [0] for elem in self.power], "J5")
            excel.write(sheet, [[self.cacMucCongSuat[1]] if elem != 0 else [0] for elem in self.power], "K5")
            excel.write(sheet, [[self.cacMucCongSuat[1]] if elem != 0 else [0] for elem in self.power], "L5")
            excel.write(sheet, [[self.cacMucCongSuat[1]] if elem != 0 else [0] for elem in self.power], "M5")
        elif len(self.cacMucCongSuat) == 3:
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "D5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "E5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "F5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "G5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "H5")
            excel.write(sheet, [[self.cacMucCongSuat[1]] if elem != 0 else [0] for elem in self.power], "I5")
            excel.write(sheet, [[self.cacMucCongSuat[1]] if elem != 0 else [0] for elem in self.power], "J5")
            excel.write(sheet, [[self.cacMucCongSuat[1]] if elem != 0 else [0] for elem in self.power], "K5")
            excel.write(sheet, [[self.cacMucCongSuat[2]] if elem != 0 else [0] for elem in self.power], "L5")
            excel.write(sheet, [[self.cacMucCongSuat[2]] if elem != 0 else [0] for elem in self.power], "M5")
        elif len(self.cacMucCongSuat) == 4:
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "D5")
            excel.write(sheet, [[self.cacMucCongSuat[0]] if elem != 0 else [0] for elem in self.power], "E5")
            excel.write(sheet, [[self.cacMucCongSuat[1]] if elem != 0 else [0] for elem in self.power], "F5")
            excel.write(sheet, [[self.cacMucCongSuat[1]] if elem != 0 else [0] for elem in self.power], "G5")
            excel.write(sheet, [[self.cacMucCongSuat[2]] if elem != 0 else [0] for elem in self.power], "H5")
            excel.write(sheet, [[self.cacMucCongSuat[2]] if elem != 0 else [0] for elem in self.power], "I5")
            excel.write(sheet, [[self.cacMucCongSuat[2]] if elem != 0 else [0] for elem in self.power], "J5")
            excel.write(sheet, [[self.cacMucCongSuat[3]] if elem != 0 else [0] for elem in self.power], "K5")
            excel.write(sheet, [[self.cacMucCongSuat[3]] if elem != 0 else [0] for elem in self.power], "L5")
            excel.write(sheet, [[self.cacMucCongSuat[3]] if elem != 0 else [0] for elem in self.power], "M5")
        
        # Write date
        date = [[date]]
        excel.write(sheet, date, 'B2')
        excel.write(sheet, date, 'N2')
        
        # write gia chao
        excel.write(sheet, self.giachao, 'D3')
        excel.write(sheet, self.giachao, 'P3')
        book.save(excel_path_out)
