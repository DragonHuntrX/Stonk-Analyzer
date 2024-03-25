from math import floor
from analyzer import Analyzer
import time

start = time.perf_counter()
analyzer = Analyzer()
analyzer.get_stonks("stock_list.csv")
analyzer.update_profiles()
end = time.perf_counter()

time = end - start
hours = floor(time / 3600)
mins = floor((time % 3600) / 60)
secs = floor(time % 60)

print("=================================================================")
print(f"\tTime taken: {hours} hours, {mins} minutess, {secs} seconds")
print("=================================================================")
