<<<<<<< HEAD
#let us create our comapnys structure by using recurtion
employees={
    "name":"CEO",
    "reports":[
        {
            "name":"Manager A",
            "reports":[
                {
                    "name":"Employee A1","reports":[]
                },
                {
                    "name":"Employee A2","reports":[]
                }
            ]
        },
        {
            "name":"Manager B",
            "reports":[
                {
                    "name":"Employee B1","reports":[]
                },
                {
                    "name":"Employee B2","reports":[]
                }
            ]
        }
    ]
}
#
def display_employees(employees,indent=2):
    print(" " * indent + employees["name"])
    for report in employees["reports"]:
        display_employees(report, indent + 4)

=======
#let us create our comapnys structure by using recurtion
employees={
    "name":"CEO",
    "reports":[
        {
            "name":"Manager A",
            "reports":[
                {
                    "name":"Employee A1","reports":[]
                },
                {
                    "name":"Employee A2","reports":[]
                }
            ]
        },
        {
            "name":"Manager B",
            "reports":[
                {
                    "name":"Employee B1","reports":[]
                },
                {
                    "name":"Employee B2","reports":[]
                }
            ]
        }
    ]
}
#
def display_employees(employees,indent=2):
    print(" " * indent + employees["name"])
    for report in employees["reports"]:
        display_employees(report, indent + 4)

>>>>>>> bb21825 (Add updates)
display_employees(employees)