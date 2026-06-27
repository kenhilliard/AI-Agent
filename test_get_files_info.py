from functions.get_files_info import get_files_info

print("Result for current directory:")
result = get_files_info("calculator", ".")
indented_result = "  " + result.replace("\n", "\n  ")
print(indented_result)

print("Result for pkg directory:")
result = get_files_info("calculator", "pkg")
indented_result = "  " + result.replace("\n", "\n  ")
print(indented_result)

print("Result for /bin directory:")
result = get_files_info("calculator", "/bin")
indented_result = "  " + result.replace("\n", "\n  ")
print(indented_result)

print("Result for ../ directory:")
result = get_files_info("calculator", "../")
indented_result = "  " + result.replace("\n", "\n  ")
print(indented_result)