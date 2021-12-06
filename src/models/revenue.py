import pandas as pd # type: ignore[import]
from typing import List, Dict, Any
from os import path
import matplotlib.pyplot as plt # type: ignore[import]
import math
from src.models.offer import Offer
from src.db import db

class Revenue:
    def __init__(
        self,
        priceContract: float,
        data: Dict[str, object],
        Pmin: float = 11.0,
        CSCB: float = 13.0,
        ceilPrice: float = 1503.5
    ) -> None:
        df = pd.DataFrame(data = data)
        offer = Offer(
            Pmin=Pmin,
            CSCB=CSCB,
            smp=db.predictions,
            power=df['Sản lượng dự kiến phát'],
            mucGiaTran=ceilPrice
        )
        self.priceContract = priceContract
        # df['Sản lượng dự kiến phát']
        sanluongdukien2  = []
        # Cach 1
        # for i, elem in enumerate(df['Sản lượng dự kiến phát']):
        #     if elem > 0:
        #         if df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= priceContract*1.5:
        #             elem = 22
        #         elif df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= priceContract*1.4:
        #             elem = 20
        #         elif df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= priceContract*1.3 :
        #             elem = 17
        #         elif df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= priceContract:
        #             elem = 14
        #         else:
        #             elem = 11
        #     sanluongdukien2.append(elem)
        
        # Cach 2:
        for i, elem in enumerate(df['Sản lượng dự kiến phát']):
            if elem > 0:
                if len(offer.cacMucCongSuat) == 4:
                    if df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-1] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-2] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-3]:
                        elem = offer.cacMucCongSuat[-1]
                    elif df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-4] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-5] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-6]:
                        elem = offer.cacMucCongSuat[-2]
                    elif df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-7] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-8]:
                        elem = offer.cacMucCongSuat[-3]
                    else:
                        elem = 11
                elif len(offer.cacMucCongSuat) == 3:
                    if df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-1] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-2]:
                        elem = offer.cacMucCongSuat[-1]  
                    elif df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-3] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-4] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-5]:
                        elem = offer.cacMucCongSuat[-2]
                    else:
                        elem = 11
                elif len(offer.cacMucCongSuat) == 2:
                    if df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-1] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-2] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-3] or \
                        df['Giá biên tham chiếu cho bản chào giá dự kiến'][i] >= offer.giachao[0][-4]:
                        elem = offer.cacMucCongSuat[-1]
                    else:
                        elem = 11
                else:
                    elem = offer.cacMucCongSuat[-1]
            sanluongdukien2.append(elem)
                

        df['Sản lượng dự kiến phát'] = sanluongdukien2
        
        
        df['Doanh thu dự kiến TT'] = df['Sản lượng hợp đồng (Qc)']*(priceContract - df['Giá biên tham chiếu cho bản chào giá dự kiến'] - df['Giá CAN']) + df['Sản lượng dự kiến phát']*(df['Giá biên tham chiếu cho bản chào giá dự kiến'] + df['Giá CAN'])
        df['Doanh thu dự kiến theo HĐ'] = df['Sản lượng dự kiến phát']*priceContract
        self.df = df
        
    def getRevenue(
        self
    ) -> Dict[str, float]:  
        return {
            'Doanh thu dự kiến TT': self.df['Doanh thu dự kiến TT'].sum(),
            'Doanh thu dự kiến theo HĐ': self.df['Doanh thu dự kiến theo HĐ'].sum(),
            'Tỷ lệ': self.df['Doanh thu dự kiến TT'].sum()/self.df['Doanh thu dự kiến theo HĐ'].sum()*100 - 100
        }
    
    def createRevenue(
        self,
        nameExcel: str = 'Bảng dự kiến doanh thu',
        date: str = 'Ngày 29/9/2021'
    ) -> None:
        root_directory = path.dirname(path.dirname(__file__))
        excel_path = path.join(root_directory, "../data", f"{nameExcel}.xlsx")
        with pd.ExcelWriter(excel_path, date_format="dd/mm/yyyy") as writer:
            startrow, startcol = 4, 0
            self.df.to_excel(writer, header=False, index=False,
                             startrow=startrow, startcol=startcol)
            book = writer.book
            sheet = writer.sheets["Sheet1"]
            sheet.write("A2", "Giá HĐ")
            sheet.write("B2", self.priceContract)
            sheet.write("A3:B3", date)
            sheet.write("A53:B53", "Tổng doanh thu")
            sheet.write("E53", self.df['Sản lượng hợp đồng (Qc)'].sum())
            sheet.write("F53", self.df['Doanh thu dự kiến TT'].sum())
            sheet.write("G53", self.df['Doanh thu dự kiến theo HĐ'].sum())
            
            format_header = book.add_format({
                'text_wrap': True,
                'align': 'center',
                'valign': 'vcenter',
                'bold': True
            })
            sheet.set_row(3, 80, format_header)
            for colx, value in enumerate(self.df.columns.values):
                sheet.write(3, colx, value)