from collections import Counter

def indexing(data):
    frequency_counter = Counter()
    # Step 3: Iterate through each object in the array
    for obj in data:
        # Step 4: Extract keys and values from each object
        for key, value in obj.items():
            # Step 5: Count frequencies of each key-value pair
            if key == "Time":
                # Count occurrences of the key "Time" itself
                frequency_counter[key] += 1
            elif key == "Description":
                # Check for special conditions in "Description" values
                if "Chamfer" in value:
                    frequency_counter["Chamfer"] += 1
                elif "Extrude" in value:
                    # Count occurrences of "Extrude" within the values of "Description"
                    frequency_counter["Extrude"] += 1
                elif "Revolute" in value:
                    frequency_counter["Revolute"] += 1
                elif "Move" in value:
                    frequency_counter["Move"] += 1
                elif "Suppress" in value:
                    frequency_counter["Suppress"] += 1
                elif "Unsuppress" in value:
                    frequency_counter["Unuppress"] += 1
                elif "Unfix" in value:
                    frequency_counter["Unfix"] += 1
                elif "Hide" in value:
                    frequency_counter["Suppress"] += 1
                elif "Insert feature" in value:
                    frequency_counter["Insert feature"] += 1
                elif "Insert tab" in value:
                    frequency_counter["Insert tab"] += 1
                elif "Edit" in value:
                    frequency_counter["Edit"] += 1
                elif "Delete" in value:
                    frequency_counter["Delete"] += 1
                elif "Copy" in value:
                    frequency_counter["Copy"] += 1
                elif "Tab Bridge" in value:
                    frequency_counter["Tab Bridge"] += 1
                elif "User StudentA1 imported" in value:
                    frequency_counter["User StudentA1 imported"] += 1
                elif "User StudentA1 exported" in value:
                    frequency_counter["User StudentA1 exported"] += 1
                elif "Change" in value:
                    frequency_counter["Change"] += 1
                elif "Tab" in value and "Assembly" in value:
                    frequency_counter["Tab: Assembly"] += 1
                elif "Tab" in value and "Part Studio" in value:
                    frequency_counter["Tab: Part Studio"] += 1
                elif "Insert new tab" in value and 'Assembly' in value:
                    frequency_counter["Insert new tab: Assembly"] += 1
                elif "Insert new tab" in value and 'Part Studio' in value:
                    frequency_counter["Insert new tab: Part Studio"] += 1
                elif "Show" in value and 'Planar' in value:
                    frequency_counter["Show: Planar"] += 1
                elif "Rename tab" in value:
                    frequency_counter["Rename tab"] += 1
                elif "Insert" in value and "Part" in value:
                    frequency_counter["Insert: Part"] += 1
                elif "Fix" in value and "Part" in value:
                    frequency_counter["Fix: Part"] += 1
                elif "Show Sketch" in value:
                    frequency_counter["Show Sketch"] += 1
                else:
                    frequency_counter[value] += 1
    return frequency_counter