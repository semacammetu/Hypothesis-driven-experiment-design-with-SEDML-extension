def test_data():
    folder_name = 'test_data/traffic_data_l6/'
    signal_file_base = 'test'
    trace_count = 20
    phi_1 = ' ( P 1 1 ( ( x1 > 15 ) & ( x7 = 1 ) & ( x6 = 0 ) ) ) '
    phi_2 = ' ( P 1 1 ( ( x1 > 25 ) & ( x7 = 1 ) ) ) '
    phi_3 = ' ( P 1 1 ( ( x4 < 10 ) & ( x7 = 1 ) & ( x6 = 0 ) ) )'
    optimized_formula = phi_1 + ' | ' + phi_2 + ' | ' + phi_3
    result = evaluator.evaluate_signals(STL.infix_to_prefix(optimized_formula), folder_name, signal_file_base, 20, '',
                                        stl_constants.__DETAILED, stn=None,
                                        past_results=[])
    print ('for formula = ' + optimized_formula + ' result is: ' + str(result))
