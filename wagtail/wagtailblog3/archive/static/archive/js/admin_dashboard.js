document.addEventListener('DOMContentLoaded', function () {
    // 初始化日期选择器
    flatpickr(".datepicker", {
        dateFormat: "Y-m-d", // 与 Django 解析格式一致
        altInput: true, // 显示一个更友好的日期格式
        altFormat: "Y年m月d日",
        locale: "zh", // 使用中文语言包
        onChange: function(selectedDates, dateStr, instance) {
            // 可选：当一个日期改变时，自动设置另一个日期的一些逻辑
            // 例如，如果开始日期晚于结束日期，则将结束日期设为开始日期
            const startDateInput = document.getElementById('id_start_date');
            const endDateInput = document.getElementById('id_end_date');
            const fpStart = startDateInput._flatpickr;
            const fpEnd = endDateInput._flatpickr;

            if (instance.element.id === 'id_start_date' && fpEnd.selectedDates.length > 0) {
                if (selectedDates[0] > fpEnd.selectedDates[0]) {
                    fpEnd.setDate(selectedDates[0], false); // false 表示不触发 onChange
                }
                fpEnd.set('minDate', selectedDates[0]); // 结束日期不能早于开始日期
            } else if (instance.element.id === 'id_end_date' && fpStart.selectedDates.length > 0) {
                if (selectedDates[0] < fpStart.selectedDates[0]) {
                    fpStart.setDate(selectedDates[0], false);
                }
                fpStart.set('maxDate', selectedDates[0]); // 开始日期不能晚于结束日期
            }
        }
    });


    // 点击查询按钮时，如果日期为空，可以给用户提示或阻止提交
    const filterForm = document.getElementById('date-filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(event) {
            const startDate = document.getElementById('id_start_date').value;
            const endDate = document.getElementById('id_end_date').value;
            if (!startDate && !endDate) {
                // 如果两个日期都为空，并且当前不是默认显示（即没有其他过滤条件），
                // 那么就按默认逻辑（显示最近10篇）
                // 如果有其他逻辑，比如必须选日期，可以在这里阻止并提示
                // console.log("No date range selected, showing recent posts.");
                // 如果希望必须选择日期才查询，则：
                // event.preventDefault();
                // alert("请选择开始日期和结束日期！");
            } else if (!startDate || !endDate) {
                event.preventDefault(); // 阻止表单提交
                alert("请同时选择开始日期和结束日期进行查询！");
            }
        });
    }
});