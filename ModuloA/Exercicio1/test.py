def test(result, expected):
    print("\n--------------TEST--------------")
    print(f"Expected output: {expected}")
    print(f"Actual output: {result}")
    if(result == expected): 
        print("Test passed")
    else:
        print("Test failed")