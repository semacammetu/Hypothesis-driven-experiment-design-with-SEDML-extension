

function [val, m_indices, v, m] = get_plot_data(results, param_indices)

% param_indices : 2 index
% val : 2 dimensional matrix, best valuations for param_indices 
% v: best valuation, m: indices of all params for best valuation
% m_indices: same size as val, gives the indices of all parameters for the 
% corresponding valuation

[val, m_indices] = max_helper(results.val, param_indices(1), param_indices(2));


[v, m] = max(val(:));

[m1, m2] = ind2sub(size(val), m);
m = squeeze(m_indices(m1,m2,:));

val = squeeze(val);
end



function [val, indexes] = max_helper(values, p1index, p2index)

s = size(values);
param_count = length(s);

indexes = zeros(s(p1index), s(p2index), param_count);
val = values;
for i=param_count:-1:1
    if ~(i == p1index || i == p2index)
        val = max(val, [], i);
    end
end

val = squeeze(val);
for p1=1:s(p1index)
    for p2=1:s(p2index)
        ind = find(values == val(p1, p2), 1);
        for i=1:param_count
            [indexes(p1, p2, i), ind] = ind2sub(s(i:end), ind);
        end
    end
end

end
