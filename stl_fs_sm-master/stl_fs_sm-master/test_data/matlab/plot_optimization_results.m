

close all;

test_names = {'test_result_P_greater_than', 'test_result_A_greater_than', 'test_result_P_A_greater_than', 'test_result_A_greater_than_500'};


test_names = {'test_result_A_greater_than', 'test_result_A_greater_than_500'};

test_names = {'test_result_P_A_greater_than'}

r=cell(length(test_names),1);
for i=1:length(test_names)
    test_name = test_names{i};
    r{i} = load(strcat('/Users/ebruaydingol/PycharmProjects/stl_fs_sm/test_data/test_from_holy/gauss_test_only_A/', test_name, '.mat'));

    param_count = length(r{i}.parameter_list);

    param_2_comb = combnk(1:param_count, 2);


    for x=1:size(param_2_comb,1)
        param_indices = param_2_comb(x,:);
        [val, m_indices, v, m] = get_plot_data(r{i}, param_indices);
        plot_for_params(val, param_indices,r{i});
    end

    figure;
    plot(r{i}.val)
    title(test_name)
end




% for the rest of the parameters, pick the best one and return it's
% indices:








