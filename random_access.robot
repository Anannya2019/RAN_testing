*** Settings ***
Documentation    Automate 5G NR Random Access Performance Testing
Library          OperatingSystem
Library          Process
Library          Collections
Library          String    # Added to provide Split To Lines
Library          ${CURDIR}/random_access.py

*** Variables ***
${LOW_UE_LOAD}    10
${MEDIUM_UE_LOAD}    50
${HIGH_UE_LOAD}    100
${VERY_HIGH_UE_LOAD}    200
${OUTPUT_DIR}    results

*** Test Cases ***
Test Low UE Load Success Rate
    [Documentation]    Ensure high success rate with low UE load
    ${simulator}=    Create Simulator Instance
    ${result}=    Run Simulation    ${simulator}    ${LOW_UE_LOAD}
    Should Be True    ${result['prach_success_rate']} >= 0.8    Success rate should be high for low load

Test Medium UE Load Collision Probability
    [Documentation]    Verify increased collision probability with medium UE load
    ${simulator}=    Create Simulator Instance
    ${result}=    Run Simulation    ${simulator}    ${MEDIUM_UE_LOAD}
    Should Be True    ${result['collision_probability']} > 0.1    Collision probability should be non-zero and noticeable

Test High UE Load Retransmissions
    [Documentation]    Check retransmissions rise with high UE load
    ${simulator}=    Create Simulator Instance
    ${result}=    Run Simulation    ${simulator}    ${HIGH_UE_LOAD}
    Log    Retransmissions for UE load ${HIGH_UE_LOAD}: ${result['retransmissions']}    level=INFO
    Should Be True    ${result['retransmissions']} > 20    Retransmissions should be significant (adjusted threshold)

Test Very High UE Load Access Delay
    [Documentation]    Verify access delay behavior with very high UE load
    ${simulator}=    Create Simulator Instance
    ${result}=    Run Simulation    ${simulator}    ${VERY_HIGH_UE_LOAD}
    Should Be True    ${result['access_delay']} == 0 or ${result['access_delay']} > 0.01    Delay should be 0 (no success) or reasonable

Test Retransmission Increase Across Loads
    [Documentation]    Confirm retransmissions increase as UE load rises from low to high
    ${simulator}=    Create Simulator Instance
    ${low_result}=    Run Simulation    ${simulator}    ${LOW_UE_LOAD}
    ${high_result}=    Run Simulation    ${simulator}    ${HIGH_UE_LOAD}
    Should Be True    ${high_result['retransmissions']} > ${low_result['retransmissions']}    Retransmissions should increase with load

Test Collision Probability Increase
    [Documentation]    Verify collision probability increases with UE load
    ${simulator}=    Create Simulator Instance
    ${med_result}=    Run Simulation    ${simulator}    ${MEDIUM_UE_LOAD}
    ${high_result}=    Run Simulation    ${simulator}    ${HIGH_UE_LOAD}
    Should Be True    ${high_result['collision_probability']} > ${med_result['collision_probability']}    Collision probability should rise

Test CSV File Creation
    [Documentation]    Ensure results are saved to CSV
    ${simulator}=    Create Simulator Instance
    Run Simulation    ${simulator}    ${LOW_UE_LOAD}
    Save Results    ${simulator}
    File Should Exist    ${OUTPUT_DIR}/results.csv

Test CSV Data Integrity
    [Documentation]    Verify CSV contains correct data after simulation
    ${simulator}=    Create Simulator Instance
    ${result}=    Run Simulation    ${simulator}    ${MEDIUM_UE_LOAD}
    Save Results    ${simulator}
    ${df}=    Import CSV    ${OUTPUT_DIR}/results.csv
    Should Be Equal As Integers    ${df[0]['ue_load']}    ${MEDIUM_UE_LOAD}    CSV should reflect UE load

Test Visualization Output
    [Documentation]    Confirm plot is generated after simulations
    ${simulator}=    Create Simulator Instance
    Run Simulation    ${simulator}    ${LOW_UE_LOAD}
    Run Simulation    ${simulator}    ${HIGH_UE_LOAD}
    Visualize Results    ${simulator}
    File Should Exist    ${OUTPUT_DIR}/results_plot.png

Test Zero UE Load Edge Case
    [Documentation]    Validate simulation with no UEs
    ${simulator}=    Create Simulator Instance
    ${result}=    Run Simulation    ${simulator}    0
    Should Be Equal    ${result['prach_success_rate']}    ${0.0}    Success rate should be 0
    Should Be Equal    ${result['retransmissions']}    ${0}    No retransmissions with no UEs

*** Keywords ***
Create Simulator Instance
    [Documentation]    Initialize the simulator
    Log    Creating RandomAccessSimulator instance    level=INFO
    ${simulator}=    Evaluate    random_access.RandomAccessSimulator('${OUTPUT_DIR}')
    Log    Simulator instance created: ${simulator}    level=INFO
    RETURN    ${simulator}

Run Simulation
    [Arguments]    ${simulator}    ${ue_load}
    [Documentation]    Run simulation for a specific UE load
    ${ue_load_int}=    Convert To Integer    ${ue_load}
    Log    Running simulation with UE load: ${ue_load_int}    level=INFO
    ${result}=    Call Method    ${simulator}    run_simulation    ${ue_load_int}
    Should Not Be Empty    ${result}
    Log    Simulation result for UE load ${ue_load}: ${result}    level=INFO
    RETURN    ${result}

Save Results
    [Arguments]    ${simulator}
    [Documentation]    Save results to CSV
    Log    Saving results to CSV    level=INFO
    Call Method    ${simulator}    save_results    csv

Visualize Results
    [Arguments]    ${simulator}
    [Documentation]    Generate visualization
    Log    Generating visualization    level=INFO
    Call Method    ${simulator}    visualize_results

Import CSV
    [Arguments]    ${file_path}
    [Documentation]    Read CSV file into a list of dictionaries
    ${content}=    Get File    ${file_path}
    ${lines}=    Split To Lines    ${content}
    ${header}=    Remove From List    ${lines}    0
    ${data}=    Create List
    FOR    ${line}    IN    @{lines}
        ${fields}=    Split String    ${line}    ,
        ${dict}=    Create Dictionary
        ...    ue_load=${fields[0]}
        ...    prach_success_rate=${fields[1]}
        ...    collision_probability=${fields[2]}
        ...    access_delay=${fields[3]}
        ...    retransmissions=${fields[4]}
        Append To List    ${data}    ${dict}
    END
    RETURN    ${data}