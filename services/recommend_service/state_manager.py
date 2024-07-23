def state_manager (vegeetarian, weight , height , exersize_level):

    weight = float(weight)
    height = float(height)
    vegeetarian = int(vegeetarian)
    exersize_level = int(exersize_level)

    BMI = weight / (height * height)

    if vegeetarian == 0:
        if BMI < 18.5:
            state = 1
        elif BMI >= 18.5 and BMI < 25:
            if exersize_level == 0:
                state = 3
            else:
                state = 1
        else:
            state = 3
            
    else:
        if BMI < 18.5:
            state = 2
        elif BMI >= 18.5 and BMI < 25:
            if exersize_level == 0:
                state = 4
            else:
                state = 2
        else:
            state = 4
       
               

    return state

def next_state_calculator (state) :
    if state == ( 1,2,4,5,7,8,10,11):
        state = state + 1
    elif state == (3 , 6 , 9 , 12):
        state = state - 2
    return state

def state_manager_v2 (vegeetarian, weight , height , exersize_level,meal):


    print (vegeetarian, weight , height , exersize_level,meal)

    weight = float(weight)
    height = float(height)
    vegeetarian = int(vegeetarian)
    exersize_level = int(exersize_level)
    meal = int(meal)

    BMI = weight / (height * height)

    if meal == 0:
        if vegeetarian == 0:
            if BMI < 18.5:
                state = 1 # breakfast non veg high cal
            elif BMI >= 18.5 and BMI < 25:
                if exersize_level == 0:
                    state = 7 #breakfast non veg low cal
                else:
                    state = 1 # breakfast non veg high cal
            else:
                state = 7 #breakfast non veg low cal
        else:
            if BMI < 18.5:
                state = 4 #breakfast veg high cal
            elif BMI >= 18.5 and BMI < 25:
                if exersize_level == 0:
                    state = 10 #breakfast veg low cal
                else:
                    state = 4 #breakfast veg high cal
            else:
                state = 10 #breakfast veg low cal
    elif meal == 1:
        if vegeetarian == 0:
            if BMI < 18.5:
                state = 2 #lunch non veg high cal
            elif BMI >= 18.5 and BMI < 25:
                if exersize_level == 0:
                    state = 8 #lunch non veg low cal
                else:
                    state = 2 #lunch non veg high cal
            else:
                state = 8 #lunch non veg low cal
        else:
            if BMI < 18.5:
                state = 5 #lunch veg high cal
            elif BMI >= 18.5 and BMI < 25:
                if exersize_level == 0:
                    state = 11 #lunch veg low cal
                else:
                    state = 5  #lunch veg high cal
            else:
                state = 11 #lunch veg low cal
    elif meal == 2:
        if vegeetarian == 0:
            if BMI < 18.5:
                state = 3 #dinner non veg high cal
            elif BMI >= 18.5 and BMI < 25:
                if exersize_level == 0:
                    state = 9 #dinner non veg low cal
                else:
                    state = 3 #dinner non veg high cal
            else:
                state = 9 #dinner non veg low cal
        else:
            if BMI < 18.5:
                state = 6 #dinner veg high cal
            elif BMI >= 18.5 and BMI < 25:
                if exersize_level == 0:
                    state = 12 #dinner veg low cal
                else:
                    state = 6 #dinner veg high cal
            else:
                state = 12 #dinner veg low cal
    else:
        state = None
       
               

    return state