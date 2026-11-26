customer_totals = {}

try:
    file = open("transactions.txt", "r")

    for line in file:
        name, amount = line.strip().split(",")
        amount = float(amount)

        if name in customer_totals:
            customer_totals[name] += amount
        else:
            customer_totals[name] = amount

    file.close()

    sorted_totals = sorted(
        customer_totals.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("Customer Summary")

    for name, total in sorted_totals:
        print(f"{name}: {total} ETB")

    report = open("report.txt", "w")

    for name, total in sorted_totals:
        report.write(f"{name}: {total} ETB\n")

    report.close()

    print("Summary written to report.txt")

except FileNotFoundError:
    print("Error: transactions.txt not found.")