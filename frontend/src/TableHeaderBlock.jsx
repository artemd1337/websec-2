
function TableHeaderBlock({week, setWeek}) {
    function NextWeekClicked(currentWeek){
        {parseInt(currentWeek) < 18 && setWeek(parseInt(currentWeek) + 1)}
    }

    function PrevWeekClicked(currentWeek){
        {parseInt(currentWeek) > 1 && setWeek(parseInt(currentWeek) - 1)}
    }

    return (
        <div className="schedule_header">
            <a className="week_button" onClick={()=> PrevWeekClicked(week)}>Предыдущая неделя</a>
            <div className="current_week">{week} неделя</div>
            <a className="week_button" onClick={()=> NextWeekClicked(week)}>Следующая неделя</a>
        </div>
    );
}

export default TableHeaderBlock;