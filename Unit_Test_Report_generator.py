import os
import re
import shutil

def run_command(command):
    """Run a system command and check for errors."""
    result = os.system(command)
    if result != 0:
        print(f"Error executing: {command}")
        exit(1)

def main():
    # Set color to green for command
    os.system("color A")

    # Ask if separate test script is needed for compound test cases
    compound_yes = input("\nDo You Want Separate Test Script for Compound Test Cases? (Y/N): ").upper()

    # Ask for module name
    module_name = input("Enter The Module Name: ")

    # Create directories for Unit test scripts and results
    os.makedirs("Unit_Tst", exist_ok=True)
    os.makedirs("Results", exist_ok=True)

    # Set environment variables
    os.environ["Unit_name"] = module_name
    os.environ["Environment_Name"] = module_name.upper()

    # Generate test script extraction for all test cases
    run_command(f"C:\\VCAST\\clicast.exe -lc -e {os.environ['Environment_Name']} TESt Script CReate {os.environ['Environment_Name']}.tst")
    shutil.copy(f"{os.environ['Environment_Name']}.tst", "Results")

    # Generate reports
    run_command(f"C:\\VCAST\\clicast.exe -lc -e {os.environ['Environment_Name']} Reports Custom MAnagement {module_name}_Testcase_Management_Report.html")
    run_command(f"C:\\VCAST\\clicast.exe -lc -e {os.environ['Environment_Name']} Reports Custom ACtual {module_name}_Execution_Results_Report.html")
    run_command(f"C:\\VCAST\\clicast.exe -lc -e {os.environ['Environment_Name']} REports Custom FULl {module_name}_Full_Report.html")

    # Copy the script to another script to avoid conflict
    with open(f"{os.environ['Environment_Name']}.tst", errors='ignore') as duplicate_data:
        with open(f"{os.environ['Environment_Name']}_copy.tst", "w+") as duplicate_data_write:
            for line in duplicate_data:
                duplicate_data_write.write(line)

    # Algorithms for generating unit reports for each function
    with open(f"{os.environ['Environment_Name']}_copy.tst", errors='ignore') as fun:
        for find_fun in fun.readlines():
            if re.search(r'\s*-- Subprogram:', find_fun, re.IGNORECASE):
                fun_name = find_fun.split()[2]
                run_command(f"C:\\VCAST\\clicast.exe -e {os.environ['Environment_Name']} -u {module_name} -s {fun_name} TESt Script CReate {fun_name}.tst")
                shutil.move(f"{fun_name}.tst", "Unit_Tst")

    if compound_yes == "Y":
        run_command(f'C:\\VCAST\\clicast.exe -e {os.environ["Environment_Name"]} -u {module_name} -s "<<COMPOUND>>" TESt Script CReate __COMPOUND__.tst')
        shutil.move("__COMPOUND__.tst", "Unit_Tst")

    # Move the results files into the results folder
    shutil.move(f"{module_name}_Full_Report.html", "Results")
    shutil.move(f"{module_name}_Execution_Results_Report.html", "Results")
    shutil.move(f"{module_name}_Testcase_Management_Report.html", "Results")

if __name__ == "__main__":
    main()
