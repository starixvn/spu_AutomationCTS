Default_Value = {
    "local" : {
        "sport" : {
            "MainSport" : ["Soccer","Basketball","E-Sports"],
            "VirtualSport" : ["Virtual Soccer", "Virtual Basketball"]
        },
        "Market" : ["All","Live","Non-Live"],
        "Event" : "League/Match",
        "MatchSection" : ["Live","Today","Early","Closed"],
        "BetType" : ["HDP","O/U","1H HDP","1H O/U"],
        "Reason" : {
            "DetectbySystem" : ["ARB","FG","GB","HED","IRR"],
            "DetectbyAI" : ["GB(P)","LB"]
        },
        "Verified" : ["All","Yes","No"],
        "Refresh" : ["None","Refresh(15)","Refresh(30)","Refresh(60)"],
        "pageSize" : ["1,000","1,500","2,000"],
        "defaultPageSize" : "1,000",
        "BTofSoccer_VirtualSoccer" : ["HDP", "O/U", "1H HDP", "1H O/U"],
        "BTofBasketball_VirtualBasketball" : ["HDP","O/U","1H HDP","1H O/U","ML","Quarter 1 HDP","Quarter 2 HDP","Quarter 3 HDP","Quarter 4 HDP","Quarter 1 O/U","Quarter 2 O/U","Quarter 3 O/U","Quarter 4 O/U","Quarter 1 ML","Quarter 2 ML","Quarter 3 ML","Quarter 4 ML",],
        "BTofESports" : ["HDP","O/U","ML","Map X ML","Map X Round Y ML","Map X Total Gold ML","Map X Total Kills HDP","Map X Total Kills O/U","Map X Total Kills O/E","Map X First Blood","Map X First to Y Kills","Map X Round Y Total Kills O/U","Map X Round Y Total Kills O/E","Map X Round Y First Kill","Map X Round Y Total Kills HDP","Map X First to Y Kills Time(Mins) O/U","Map X First Blood Time(Mins) O/U","Map X Total Kills at 10 Mins HDP","Map X Total Kills at 10 Mins O/U","Map X Total Kills at 20 Mins HDP","Map X Total Kills at 20 Mins O/U","Map X Home Team Total Kills at 10 Mins O/U","Map X Away Team Total Kills at 10 Mins O/U","Map X Home Team Total Kills at 20 Mins O/U","Map X Away Team Total Kills at 20 Mins O/U","Map X Home Team Total Kills O/U","Map X Away Team Total Kills O/U","Map X 1st Kill","Map X 2nd Kill","Map X 3rd Kill","Map X 4th Kill","Map X 5th Kill","Map X 6th Kill","Map X 7th Kill","Map X 8th Kill","Map X 9th Kill","Map X 10th Kill","Map X 15th Kill","Map X 20th Kill","Map X Will Storm Dragon Be Killed Yes/No","Map X Will Elder Dragon Be Killed Yes/No",],
    },
    "pro" : {
        "sport" : {
            "MainSport" : ["Soccer","Basketball","E-Sports"],
            "VirtualSport" : ["Virtual Soccer", "Virtual Basketball"]
        },
        "Market" : ["All","Live","Non-Live"],
        "MatchSection" : ["Live","Today","Early","Closed"],
        "BetType" : ["HDP","O/U","1H HDP","1H O/U"],
        "Reason" : {
            "DetectbySystem" : ["ARB","FG","GB","HED","IRR"],
            "DetectbyAI" : ["LB"]
        },
        "Verified" : ["All","Yes","No"],
        "Refresh" : ["None","Refresh(15)","Refresh(30)","Refresh(60)"],
        "pageSize" : ["1,000","1,500","2,000"],
        "defaultPageSize" : "1,000"
    }
}

TextError = {
    "local" : {
        "errDayGreater2" : "Invalid date range, please select not more than 2 days",
        "transtimeConvert" : "Convert to the correct Transtime format (dd/mm/yy hh:mm:ss) ?",
        "ErrDetectAssociation" : "Please select at least 2 Usernames to proceed!",
    },
    "pro" : {
        "errDayGreater2" : "Invalid date range, please select not more than 2 days"
    }
}

Value_Search = {
    "local" : {
        #------Value To Check Err Messages-----#
        "fromDateCheckErr" : "Mar 03, 2024",
        "toDateCheckErr" : "Mar 05, 2024",
    }
}