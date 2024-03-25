from analyzer import Analyzer
import time

start = time.perf_counter()
analyzer = Analyzer()
analyzer.get_stonks("stock_list.csv")
analyzer.update_profiles()
end = time.perf_counter()

print("=============================================")
print("\tTime taken:", end - start)
print("=============================================")
