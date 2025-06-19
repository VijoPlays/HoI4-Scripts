from itertools import product

from pathlib import Path
Path("results").mkdir(exist_ok=True)

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

switch_after_days = 3000
switch_con_after_days = 3000 

infra_modifiers = [1 + 0.2 * i for i in range(6)]

def consumer_goods_rounding(value):
    whole = int(value)
    first_decimal = int((value - whole) * 10)
    return whole + 1 if first_decimal >= 2 else whole

def simulate_build(econ, construction_modifiers, consumer_goods, max_infra_level, infra_level_base, total_starting_factories, mil_factories, switch_after_days = 300000, switch_con_after_days = 30000):
    """
    If your starting_factories are higher than 15, this script does not account for this! Infrastructure would perform worse in this case, since we can use the Civ Factories everywhere, but we would only benefit from the Infrastructure in this one state that got infra'd
    Mil factories are also not accounted for: When producing them you'd want them ASAP anyway, so you can produce the most equipment anyway

    total_starting_factories = Civ and Mil factories combined
    """
    days = 1
    infra_spammer_factories = total_starting_factories
    civ_greeder_factories = total_starting_factories
    infra_level_upgraded = infra_level_base    # infra_level_upgraded is the level of infrastructure that the infrastructure_spammer would get
    finished_building_infra = False

    infra_output_modifier = 1 + construction_modifiers
    civ_output_modifier = econ_laws[econ] + construction_modifiers

    def calc_factories_after_consumer_goods(total_factories):
        usable = consumer_goods_rounding(total_factories * (1 - consumer_goods) - mil_factories)
        if usable < 1:
            return 0
        return usable

    def calc_total_factory_output(total_factories, is_building_infra, infra_level_upgrade):
        if is_building_infra:
            output_mod = infra_output_modifier
        else:
            output_mod = civ_output_modifier
        
        usable_factories = calc_factories_after_consumer_goods(total_factories)
        
        boosted_factories = min(15, usable_factories)
        non_boosted_factories = usable_factories - boosted_factories

        boosted_output = boosted_factories * base_output * output_mod * infra_modifiers[infra_level_upgrade]
        normal_output = non_boosted_factories * base_output * output_mod * infra_modifiers[infra_level_base]

        return round(boosted_output + normal_output, 2)

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
        # Also modify consumer_goods if you change the econ law
        new_econ_law = 'No Economy'
        if days == switch_after_days:
            # consumer_goods = 0.27
            econ = new_econ_law
            civ_output_modifier = econ_laws[new_econ_law] + construction_modifiers
            civ_greeder_factory_output = calc_total_factory_output(civ_greeder_factories, False, infra_level_base)
            infra_spammer_factory_output = calc_total_factory_output(infra_spammer_factories, finished_building_infra, infra_level_upgraded)

        if days == switch_con_after_days:
            construction_modifiers = 0.35
            civ_output_modifier = econ_laws[econ] + construction_modifiers
            civ_greeder_factory_output = calc_total_factory_output(civ_greeder_factories, False, infra_level_base)
            infra_output_modifier = 1 + construction_modifiers
            infra_spammer_factory_output = calc_total_factory_output(infra_spammer_factories, finished_building_infra, infra_level_upgraded)

        infra_spammer_build_time -= infra_spammer_factory_output
        civ_greeder_build_time -= civ_greeder_factory_output

        if infra_spammer_build_time <= 0:
            # print(str(days))
            if infra_level_upgraded < max_infra_level:
                infra_level_upgraded += 1
                if infra_level_upgraded < max_infra_level:
                    infra_spammer_build_time = infra_build_cost
                    infra_spammer_factory_output = calc_total_factory_output(infra_spammer_factories, True, infra_level_upgraded)
                else:
                    finished_building_infra = True
                    infra_spammer_build_time = civ_factory_cost
                    infra_spammer_factory_output = calc_total_factory_output(infra_spammer_factories, False, infra_level_upgraded)
            else:
                infra_spammer_factories += 1
                infra_spammer_build_time = civ_factory_cost
                infra_spammer_factory_output = calc_total_factory_output(infra_spammer_factories, False, infra_level_upgraded)

        if civ_greeder_build_time <= 0:
            civ_greeder_factories += 1
            civ_greeder_build_time = civ_factory_cost
            civ_greeder_factory_output = calc_total_factory_output(civ_greeder_factories, False, infra_level_base)

        # Calculate the exact moment that infrastructure has more (progress) towards factories
        if finished_building_infra and infra_spammer_factories == civ_greeder_factories:
            if infra_spammer_build_time < civ_greeder_build_time:
                break

        if days == 20000:
            print("Breaking out; Ignore the next line - infra is not worth it in this case.")
            break

    # Calculate how many factories needed to be built
    infra_spammer_factories -= total_starting_factories
    civ_greeder_factories -= total_starting_factories

    # print("Total days until infra produced more: " + str(days) + ".")
    # print("Infra spammer factories: " + str(infra_spammer_factories) + ".")
    # print("Civ greeder factories: " + str(civ_greeder_factories) + ".")
    # print("-----------------------")
    return infra_spammer_factories, civ_greeder_factories, days

def calculate_total_starting_factories(mils, cg_percent, usable_civs_goal):
    """
    Returns the amount of factories needed in order to reach "usable_civs_goal" as the Civilian Factories that you can build with.
    """
    total_factories = mils
    while True:
        cg_factories = consumer_goods_rounding(total_factories * cg_percent)
        usable_civs = total_factories - mils - cg_factories + 1
        if usable_civs == usable_civs_goal:
            return total_factories
        total_factories += 1

# print(calculate_total_starting_factories(20, .2, 10))

infra_levels_to_consider = [3]
for infra in infra_levels_to_consider:
    factories, _, days = simulate_build(
        econ='No Economy', 
        construction_modifiers=0.15, 
        consumer_goods=0.20, 
        max_infra_level=4, 
        infra_level_base=infra, 
        total_starting_factories=calculate_total_starting_factories(20, .2, 10), 
        mil_factories=20,
        switch_after_days=10000,
        switch_con_after_days=100000,
        )
    print(f"Infrastructure wins with {factories} Factories after {days} days.")

def run_all_simulations():
    infra_levels = [(2, 3), (3, 4), (4, 5), (3, 5)]
    econ_laws = ['No Economy', 'Civilian Economy', 'Civ Econ Switch']
    construction_modifiers = [0.0, 0.15, 0.35]
    cgf_values = [0.4, 0.2, 0.1] # 0.4
    civ_factories_after_cgf = [10, 15] # 1, 5
    mil_factories = [0, 10, 20]

    for (start, end), econ, construction_mod, cgf, mils, civs_after_cfg in product(infra_levels, econ_laws, construction_modifiers, cgf_values, mil_factories, civ_factories_after_cgf):
        switch_after_days = 3000000
        switch_con_after_days = 3000000

        if econ == 'Civ Econ Switch':
            econ = 'Civilian Economy'
            switch_after_days = 100
        
        if construction_mod == 0.35:
            construction_mod = 0.15
            switch_con_after_days = 100

        starty_facty = calculate_total_starting_factories(mils, cgf, civs_after_cfg)
        result = simulate_build(
            econ=econ, 
            construction_modifiers=construction_mod, 
            consumer_goods=cgf, 
            max_infra_level=end, 
            infra_level_base=start, 
            total_starting_factories=starty_facty, 
            mil_factories=mils,
            switch_after_days=switch_after_days,
            switch_con_after_days=switch_con_after_days
            )
        
        if switch_con_after_days == 100:
            construction_mod = 0.35

        if switch_after_days == 100:
            econ = 'Civ Econ Switch'
        
        days = result[2]

        print(f"Infra: {start}->{end}, Con: {construction_mod}, Econ: {econ}, CGF={cgf}, Mils={mils}, Fac={civs_after_cfg} => Days: {days}, Infra Fac: {int(result[0])}")
        

# run_all_simulations()

# print("Finished calculating all infra levels, congratulations!")
