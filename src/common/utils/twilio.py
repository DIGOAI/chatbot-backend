def render_twilio_template(template: str, *args):
    for i, arg in enumerate(args, 1):
        placeholder = "{{" + str(i) + "}}"
        template = template.replace(placeholder, arg)
    return template
