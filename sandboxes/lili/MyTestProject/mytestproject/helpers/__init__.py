

def add_percentage_to_bar(bar):
    total_percentage = 0
    # Initial percentages
    for segment in bar['segments']:
        percentage = int(round(100.0 * segment['student_count'] / bar['student_count']))
        total_percentage += percentage
        segment['student_percentage'] = percentage
    # Fix percentages to add up to 100
    used_segments = []
    while total_percentage != 100 and len(used_segments) < len(bar['segments']):
        # Find largest percentage
        largest, largest_index = bar['segments'][0]['student_percentage'], 0
        for index, segment in enumerate(bar['segments']):
            if segment['student_percentage'] > largest:
                largest, largest_index = segment['student_percentage'], index
        used_segments.append(largest_index)
        # Modify percentage by one point, unless it's below 2 (too small to modify safely)
        if largest >= 2:
            if total_percentage > 100:
                bar['segments'][largest_index]['student_percentage'] -= 1
                total_percentage -= 1
            else:
                bar['segments'][largest_index]['student_percentage'] += 1
                total_percentage += 1
