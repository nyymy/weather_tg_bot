def cloud_percentage_to_emoji(cloud_percentage):
    if cloud_percentage < 20:
        return "☀️"
    elif cloud_percentage < 40:
        return "🌤️"
    elif cloud_percentage < 60:
        return "🌥️"
    else:
        return "☁️"
