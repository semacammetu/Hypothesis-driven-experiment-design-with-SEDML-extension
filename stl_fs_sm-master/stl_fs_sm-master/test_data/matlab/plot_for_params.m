function plot_for_params(val, param_indices, results)


figure;
X = results.parameter_domain{param_indices(1)};
Y = results.parameter_domain{param_indices(2)};

[X,Y] = meshgrid(X, Y);

surf(X,Y, val');
formula_t = 'A 0 p1 P 0 p2 p > p3';
if isfield(results, 'formula')
    formula_t = results.formula;
end
title( strcat('Max valuations over parameters ', ...
    results.parameter_list(param_indices(1), :), ' - ', ...
    results.parameter_list(param_indices(2), :), ' formula ',...
    formula_t));

xlabel(results.parameter_list(param_indices(1), :));
ylabel(results.parameter_list(param_indices(2), :));


end