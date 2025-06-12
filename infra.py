infra_build_cost = 6000
civ_factory_cost = 10800
base_output = 5

econ_laws = {
    'Civilian Economy': 0.7,
    'Early Mobilization': 0.9,
    'No Economy': 1.0, # Dummy law, since Civ Econ is not modified by anything above Early Mob
    # 'War Economy': 1.1,
    # 'Total Mobilization': 1.3
}

trade_laws = {
    'Free Trade': 0.15,
    'Export Focus': 0.1,
    'Limited Exports': 0.05,
    'Closed Economy': 0.0
}

infra_modifiers = [1 + 0.2 * i for i in range(6)]

def simulate_build(econ, construction_modifiers, consumer_goods, max_infra_level, infra_level_base, total_starting_factories, mil_factories):
    """
    If your starting_factories are higher than 15, this script does not account for this! Infrastructure would perform worse in this case, since we can use the Civ Factories everywhere, but we would only benefit from the Infrastructure in this one state that got infra'd
    Mil factories are also not accounted for: When producing them you'd want them ASAP anyway, so you can produce the most equipment anyway

    total_starting_factories = Civ and Mil factories combined
    """
    print("Starting loop for infrastructure level: " + str(infra_level_base) + ".")
    days = 1
    infra_spammer_factories = total_starting_factories
    civ_greeder_factories = total_starting_factories
    infra_level_upgraded = infra_level_base    # infra_level_upgraded is the level of infrastructure that the infrastructure_spammer would get
    break_even_found = False


    infra_output_modifier = 1 + construction_modifiers
    civ_output_modifier = econ_laws[econ] + construction_modifiers

    def consumer_goods_rounding(value):
        whole = int(value)
        first_decimal = int((value - whole) * 10)
        return whole + 1 if first_decimal >= 2 else whole

    def calc_factories_after_consumer_goods(total_factories):
        usable = consumer_goods_rounding(total_factories * (1 - consumer_goods) - mil_factories)
        if usable < 1:
            return 0
        return usable

    def calc_total_factory_output(total_factories, is_building_infra, infra_level):
        if is_building_infra:
            output_mod = infra_output_modifier
        else:
            output_mod = civ_output_modifier
        
        res = round(calc_factories_after_consumer_goods(total_factories) * base_output * output_mod * infra_modifiers[infra_level], 2)
        return res

    civ_greeder_build_time = civ_factory_cost
    civ_greeder_factory_output = calc_total_factory_output(civ_greeder_factories, False, infra_level_base)
    
    if infra_level_upgraded < max_infra_level:
        infra_spammer_build_time = infra_build_cost
        infra_spammer_factory_output = calc_total_factory_output(infra_spammer_factories, True, infra_level_upgraded)
    else:
        infra_spammer_build_time = civ_factory_cost
        infra_spammer_factory_output = calc_total_factory_output(infra_spammer_factories, False, infra_level_upgraded)
    
    while True:
        days += 1

        # Modify the 2 variables below and uncomment them to simulate switching econ law after x days (do a similar thing, if you want to boost infrastructure build time via e.g. Italy 25% Infra construction boost)
        # new_econ_law = 'No Economy'
        # switch_after_days = 400
        # if days == switch_after_days:
        #     civ_output_modifier = econ_laws[new_econ_law] + construction_modifiers
        #     civ_greeder_factory_output = calc_total_factory_output(civ_greeder_factories, False, infra_level_base)

        infra_spammer_build_time -= infra_spammer_factory_output
        civ_greeder_build_time -= civ_greeder_factory_output

        if infra_spammer_build_time <= 0:
            print(str(days))
            if infra_level_upgraded < max_infra_level:
                infra_level_upgraded += 1
                if infra_level_upgraded < max_infra_level:
                    infra_spammer_build_time = infra_build_cost
                else:
                    infra_spammer_build_time = civ_factory_cost
                    infra_spammer_factory_output = calc_total_factory_output(infra_spammer_factories, False, infra_level_upgraded)
            else:
                infra_spammer_factories += 1
                infra_spammer_build_time = civ_factory_cost
                infra_spammer_factory_output = calc_total_factory_output(infra_spammer_factories, False, infra_level_upgraded)

        if civ_greeder_build_time <= 0:
            # print(str(days))
            civ_greeder_factories += 1
            civ_greeder_build_time = civ_factory_cost
            civ_greeder_factory_output = calc_total_factory_output(civ_greeder_factories, False, infra_level_base)

        if infra_spammer_factories > total_starting_factories:
            if infra_spammer_factories == civ_greeder_factories and not break_even_found:
                # Keep in mind: break even does not mean break even! It can mean that the civ_greeder is almost finished with one factory and the infra_spammer just got their factory - the most accurate one is to find out when the infra_spammer has more factories than the civ_greeder
                print("break even @: " + str(days) + " days. Built factories: " + str(infra_spammer_factories - total_starting_factories))
                break_even_found = True
            if infra_spammer_factories > civ_greeder_factories:
                break

    # Calculate how many factories needed to be built
    infra_spammer_factories -= total_starting_factories
    civ_greeder_factories -= total_starting_factories

    print("Total days until infra produced more: " + str(days) + ".")
    print("Infra spammer factories: " + str(infra_spammer_factories) + ".")
    print("Civ greeder factories: " + str(civ_greeder_factories) + ".")
    print("-----------------------")
    return infra_spammer_factories, days

infra_levels_to_consider = [3]
for infra in infra_levels_to_consider:
    simulate_build(
        econ='Civilian Economy', 
        construction_modifiers=0.15, 
        consumer_goods=0.38, 
        max_infra_level=4, 
        infra_level_base=infra, 
        total_starting_factories=35, 
        mil_factories=11
        )

print("Finished calculating all infra levels, congratulations!")
