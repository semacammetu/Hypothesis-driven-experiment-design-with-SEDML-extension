
fs = 32;
three_plot = false;

test_folder = '../gaussian_test/';
for test_index=0:1:19
    
test_name = strcat('sgtest_', num2str(test_index));
test_name = strcat(test_name, '_0');


test_file = strcat(test_folder, test_name);
label_file = strcat(test_file, '_label');
SAVE = false; 
td = load(test_file);
ld = load(label_file);

m = mean(td);
M = max(td(:,2))*1.1;

if three_plot
    figure('position',[10 10 600 1500]);

    subplot(3,1,1); hold on;
    plot(td(:,1), td(:,2), '-', 'linewidth', 2)
    plot(ld(:,1), ld(:,2)*M, '-', 'linewidth', 3)
    set(gca,'fontsize',fs-4);
    grid on;



    ws = [5,10,20,40];
    ts = length(ws);
    l = cell(ts,1);
    subplot(3, 1, 2); hold on;
    for i=1:ts
        x = ws(i);
        moving_mean = movmean(td(:,2), x);
        l{i} = strcat('mean', num2str(x));

        plot(moving_mean, 'linewidth', 2);
    end
    set(gca,'fontsize',fs-4);
    legend(l)
    grid on;

    subplot(3, 1, 3); hold on;
    for i=1:length(ws)
        x = ws(i);
        moving_var = movvar(td(:,2), x);
        l{i} = strcat('var', num2str(x));

        plot(moving_var, 'linewidth', 2);
    end
    legend(l)
    grid on;
    set(gca,'fontsize',fs-4);

    if SAVE
        matlab_figure = strcat(test_file, '_mf_mean_var');
        saveas(gcf, matlab_figure, 'png');
    end

end
figure('position',[10 10 810 610]);
hold on;
plot(td(:,1), td(:,2), '-', 'linewidth', 2)
plot(ld(:,1), ld(:,2)*M, '-', 'linewidth', 3)
set(gca,'fontsize',fs-4);
grid on;
ylim([0 80]);
if SAVE
    matlab_figure = strcat(test_file, 'plot');
    saveas(gcf, matlab_figure, 'png');
end


end

