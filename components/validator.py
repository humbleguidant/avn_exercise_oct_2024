import re
# creating a function for input taking input value and regex expression as an argument
def validator(input_field, regex):
    # if input field value is valid
    return re.fullmatch(regex, input_field)
