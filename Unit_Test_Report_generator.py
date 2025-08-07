#!/usr/bin/env python3
"""
Unit Test Report Generator for VectorCAST

This script automates the generation of unit test scripts and comprehensive 
reports for software modules using VectorCAST CLI tools. It provides an 
interactive workflow for creating organized test artifacts and detailed 
reporting for quality assurance processes.

Author: Unit Test Generator Team
Version: 2.0.0
License: MIT
"""

import os
import re
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple


class UnitTestReportGenerator:
    """
    A comprehensive unit test report generator for VectorCAST environments.
    
    This class automates the creation of unit test scripts, generates various
    types of reports, and organizes test artifacts in a structured manner.
    """
    
    # Default VectorCAST installation path
    DEFAULT_VCAST_PATH = r"C:\VCAST\clicast.exe"
    
    # Directory names for organization
    DIRECTORIES = {
        'unit_tests': 'Unit_Tst',
        'results': 'Results'
    }
    
    # Report types and their corresponding CLI commands
    REPORT_TYPES = {
        'management': ('MAnagement', '_Testcase_Management_Report.html'),
        'execution': ('ACtual', '_Execution_Results_Report.html'),
        'full': ('FULl', '_Full_Report.html')
    }
    
    def __init__(self, vcast_path: str = None):
        """
        Initialize the Unit Test Report Generator.
        
        Args:
            vcast_path (str, optional): Path to VectorCAST CLI executable.
                                       Defaults to standard installation path.
        """
        self.vcast_path = vcast_path or self.DEFAULT_VCAST_PATH
        self.module_name = ""
        self.environment_name = ""
        self.include_compound_tests = False
        
        # Validate VectorCAST installation
        self._validate_vcast_installation()
    
    def _validate_vcast_installation(self) -> None:
        """
        Validate that VectorCAST is properly installed and accessible.
        
        Raises:
            FileNotFoundError: If VectorCAST CLI is not found at the specified path.
        """
        if not Path(self.vcast_path).exists():
            raise FileNotFoundError(
                f"VectorCAST CLI not found at: {self.vcast_path}\n"
                f"Please ensure VectorCAST is properly installed or update the path."
            )
    
    def _execute_command(self, command: str) -> None:
        """
        Execute a system command with error handling.
        
        Args:
            command (str): The system command to execute
            
        Raises:
            SystemExit: If the command execution fails
        """
        print(f"📋 Executing: {command}")
        result = os.system(command)
        
        if result != 0:
            print(f"❌ Error executing command: {command}")
            print(f"   Return code: {result}")
            sys.exit(1)
        print("✅ Command executed successfully")
    
    def _setup_environment(self) -> None:
        """Set up environment variables for VectorCAST operations."""
        os.environ["Unit_name"] = self.module_name
        os.environ["Environment_Name"] = self.environment_name
        print(f"🔧 Environment configured for module: {self.module_name}")
    
    def _create_directory_structure(self) -> None:
        """Create necessary directories for organizing test artifacts."""
        print("📁 Creating directory structure...")
        
        for purpose, directory_name in self.DIRECTORIES.items():
            Path(directory_name).mkdir(exist_ok=True)
            print(f"   Created: {directory_name}/")
    
    def _get_user_inputs(self) -> None:
        """
        Collect user inputs for test generation configuration.
        
        This method handles user interaction for:
        - Module name specification
        - Compound test case preferences
        """
        print("\n" + "="*60)
        print("🚀 UNIT TEST REPORT GENERATOR")
        print("="*60)
        
        # Get module name
        while True:
            self.module_name = input("\n📝 Enter the Module Name: ").strip()
            if self.module_name:
                break
            print("❌ Module name cannot be empty. Please try again.")
        
        self.environment_name = self.module_name.upper()
        
        # Get compound test preference
        while True:
            compound_input = input(
                "\n🔄 Do you want separate test scripts for Compound Test Cases? (Y/N): "
            ).strip().upper()
            
            if compound_input in ['Y', 'YES']:
                self.include_compound_tests = True
                break
            elif compound_input in ['N', 'NO']:
                self.include_compound_tests = False
                break
            else:
                print("❌ Please enter 'Y' for Yes or 'N' for No.")
        
        print(f"\n✅ Configuration complete:")
        print(f"   Module: {self.module_name}")
        print(f"   Environment: {self.environment_name}")
        print(f"   Compound Tests: {'Enabled' if self.include_compound_tests else 'Disabled'}")
    
    def _generate_main_test_script(self) -> None:
        """Generate the main test script for all test cases."""
        print("\n📜 Generating main test script...")
        
        test_script_name = f"{self.environment_name}.tst"
        command = (
            f'"{self.vcast_path}" -lc -e {self.environment_name} '
            f'TESt Script CReate {test_script_name}'
        )
        
        self._execute_command(command)
        
        # Copy to results directory
        shutil.copy(test_script_name, self.DIRECTORIES['results'])
        print(f"📋 Main test script copied to {self.DIRECTORIES['results']}/")
    
    def _generate_reports(self) -> None:
        """Generate all types of VectorCAST reports."""
        print("\n📊 Generating comprehensive reports...")
        
        for report_name, (cli_command, file_suffix) in self.REPORT_TYPES.items():
            report_filename = f"{self.module_name}{file_suffix}"
            command = (
                f'"{self.vcast_path}" -lc -e {self.environment_name} '
                f'Reports Custom {cli_command} {report_filename}'
            )
            
            print(f"   Generating {report_name} report...")
            self._execute_command(command)
    
    def _extract_function_names(self) -> List[str]:
        """
        Extract function names from the test script file.
        
        Returns:
            List[str]: A list of function names found in the test script
        """
        print("\n🔍 Extracting function names from test script...")
        
        source_file = f"{self.environment_name}.tst"
        copy_file = f"{self.environment_name}_copy.tst"
        function_names = []
        
        try:
            # Create a working copy to avoid conflicts
            with open(source_file, 'r', encoding='utf-8', errors='ignore') as source:
                with open(copy_file, 'w', encoding='utf-8') as copy:
                    content = source.read()
                    copy.write(content)
            
            # Extract function names using regex
            with open(copy_file, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    # Look for subprogram definitions
                    match = re.search(r'\s*-- Subprogram:\s*(\S+)', line, re.IGNORECASE)
                    if match:
                        function_name = match.group(1)
                        function_names.append(function_name)
                        print(f"   Found function: {function_name}")
            
            print(f"✅ Extracted {len(function_names)} function names")
            return function_names
            
        except FileNotFoundError:
            print(f"❌ Error: Test script file '{source_file}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error extracting function names: {e}")
            sys.exit(1)
    
    def _generate_individual_test_scripts(self, function_names: List[str]) -> None:
        """
        Generate individual test scripts for each function.
        
        Args:
            function_names (List[str]): List of function names to generate scripts for
        """
        print("\n🔨 Generating individual test scripts...")
        
        for function_name in function_names:
            script_filename = f"{function_name}.tst"
            command = (
                f'"{self.vcast_path}" -e {self.environment_name} '
                f'-u {self.module_name} -s {function_name} '
                f'TESt Script CReate {script_filename}'
            )
            
            print(f"   Generating script for: {function_name}")
            self._execute_command(command)
            
            # Move to unit test directory
            try:
                shutil.move(script_filename, self.DIRECTORIES['unit_tests'])
                print(f"   Moved {script_filename} to {self.DIRECTORIES['unit_tests']}/")
            except Exception as e:
                print(f"⚠️  Warning: Could not move {script_filename}: {e}")
    
    def _generate_compound_test_script(self) -> None:
        """Generate compound test script if requested by user."""
        if not self.include_compound_tests:
            return
        
        print("\n🔄 Generating compound test script...")
        
        compound_script = "__COMPOUND__.tst"
        command = (
            f'"{self.vcast_path}" -e {self.environment_name} '
            f'-u {self.module_name} -s "<<COMPOUND>>" '
            f'TESt Script CReate {compound_script}'
        )
        
        self._execute_command(command)
        
        # Move to unit test directory
        try:
            shutil.move(compound_script, self.DIRECTORIES['unit_tests'])
            print(f"📋 Compound test script moved to {self.DIRECTORIES['unit_tests']}/")
        except Exception as e:
            print(f"⚠️  Warning: Could not move compound script: {e}")
    
    def _organize_results(self) -> None:
        """Move all generated report files to the results directory."""
        print("\n📦 Organizing generated files...")
        
        results_dir = self.DIRECTORIES['results']
        
        for report_name, (_, file_suffix) in self.REPORT_TYPES.items():
            report_filename = f"{self.module_name}{file_suffix}"
            try:
                shutil.move(report_filename, results_dir)
                print(f"   Moved {report_filename} to {results_dir}/")
            except Exception as e:
                print(f"⚠️  Warning: Could not move {report_filename}: {e}")
    
    def _cleanup_temporary_files(self) -> None:
        """Clean up temporary files created during processing."""
        temp_files = [
            f"{self.environment_name}_copy.tst"
        ]
        
        for temp_file in temp_files:
            try:
                if Path(temp_file).exists():
                    os.remove(temp_file)
                    print(f"🧹 Cleaned up temporary file: {temp_file}")
            except Exception as e:
                print(f"⚠️  Warning: Could not remove temporary file {temp_file}: {e}")
    
    def _display_summary(self, function_count: int) -> None:
        """
        Display a summary of the generation process.
        
        Args:
            function_count (int): Number of functions processed
        """
        print("\n" + "="*60)
        print("🎉 UNIT TEST GENERATION COMPLETE!")
        print("="*60)
        print(f"📊 Summary:")
        print(f"   Module: {self.module_name}")
        print(f"   Functions Processed: {function_count}")
        print(f"   Reports Generated: {len(self.REPORT_TYPES)}")
        print(f"   Compound Tests: {'Included' if self.include_compound_tests else 'Not included'}")
        print(f"\n📁 Output Directories:")
        print(f"   Unit Test Scripts: {self.DIRECTORIES['unit_tests']}/")
        print(f"   Reports & Results: {self.DIRECTORIES['results']}/")
        print("\n✅ All operations completed successfully!")
    
    def run(self) -> None:
        """
        Main execution method that orchestrates the entire test generation process.
        """
        try:
            # Set console color (Windows-specific enhancement)
            if os.name == 'nt':  # Windows
                os.system("color A")  # Green text
            
            # Interactive setup
            self._get_user_inputs()
            self._setup_environment()
            self._create_directory_structure()
            
            # Generate main artifacts
            self._generate_main_test_script()
            self._generate_reports()
            
            # Extract and process functions
            function_names = self._extract_function_names()
            self._generate_individual_test_scripts(function_names)
            self._generate_compound_test_script()
            
            # Finalize organization
            self._organize_results()
            self._cleanup_temporary_files()
            
            # Display completion summary
            self._display_summary(len(function_names))
            
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            print("Please check your VectorCAST installation and try again.")
            sys.exit(1)


def main():
    """
    Entry point for the Unit Test Report Generator script.
    """
    try:
        generator = UnitTestReportGenerator()
        generator.run()
    except FileNotFoundError as e:
        print(f"❌ Setup Error: {e}")
        print("\nPlease ensure VectorCAST is properly installed and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
