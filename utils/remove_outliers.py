def remove_outliers(data, key):
    # define range
    range = 10 if key == "m2" else 10
    # Get values of all keys in data diccionary
    values = [e[key] for e in data]
    # Get q1 and q3
    q1 = sorted(values)[len(values) // 4]
    q3 = sorted(values)[len(values) * 3 // 4]
    # Calculate IQR
    iqr = q3 - q1
    # Calculate lower and upper
    lower = q1 - range * iqr
    upper = q3 + range * iqr
    #    print(iqr, q1, q3, lower, upper)
    # Return values filter without outliersfor item in data:
    #    inliers = []
    #    outliers = []

    #    for item in data:
    #        if lower <= item[key] <= upper:
    #            inliers.append(item)
    #        else:
    #            print("--", item)
    #            outliers.append(item)
    #    return inliers

    return [item for item in data if lower <= item[key] and item[key] <= upper]
