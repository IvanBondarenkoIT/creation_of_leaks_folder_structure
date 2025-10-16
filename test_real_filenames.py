"""
Test filename analyzer with real filenames from user's terminal output
"""

from filename_analyzer import FilenameAnalyzer

# Real filenames from terminal
real_filenames = [
    "Goods_byy mega.txt",
    "VIETNAM.txt",
    "DENMARK.txt",
    "INDONESIA.txt",
    "CANADA.txt",
    "SPAIN.txt",
    "vALID Byy Mega.txt",
    "Validd Good.txt",
    "VALID BY MEGA.txt",
    "Fresh Valid byy MEGACLOUD.txt",
    "Byy Mega.txt",
    "vALID mAIL.txt",
    "Hotmail_.txt",
    "PhonePass_United_State.txt",
    "HQ_FRANCE_fresh App Byy mega.txt",
    "hotmail Frash.txt",
    "Germany.txt",
    "VALID By.Mega.txt",
    "200K.txt",
    "POLAND_MAIL_ACCESS.txt",
    "VAlid.txt",
    "amazon_test.txt",
    "Mix OK.txt",
    "Hotmail 05.01.txt",
    "SOOO GOOD BYY MEGA.txt",
    "_Amazon_part 2.txt",
    "germany (1).txt",
    "Valid_mix good.txt",
    "Hotmail_part 3.txt",
    "SOOO VALID BYY MEGA.txt",
    "BYY MEGACLOUD.txt",
    "Valid byy mega Part2.txt",
    "hotmail_Fresh.txt",
    "Valid part 3.txt",
    "OK Valid.txt",
    "NUM PASS USA.txt",
    "Valid byy Megacloud part 5.txt",
    "hotmail.txt",
    "HOTMAIL AK.txt",
    "HOTMAIL good Combo.txt",
    "MIX VAlid byy mega.txt",
    "hotmail__AK.txt",
    "VALID 06.01.txt",
    "Combos Valid.txt",
    "Files_06.01_Byy mega.txt",
    "ITALI VALID.txt",
    "So sos so Valid Byy Mega.txt",
    "usa valid mail.txt",
    "Mega Valid Cloud.txt",
    "VALID MIX BY CLOUD.txt",
    "HOTMAIL Good.txt",
    "Hotmail ..txt",
    "Mega Valid.txt",
    "VALID MIX Part5.txt",
    "POLAND VALID.txt",
    "office365.txt",
    "So MEGA VALID Fresh.txt",
    "VALID GOOD.txt",
    "VALID GOOD 2.txt",
    "10k Goods_1.txt",
    "Num Pass USA (1).txt",
    "Ok__Mix Valid.txt",
    "_UK_COMBO_Valid.txt",
    "Gmail Fresh.txt",
    "Sooo Val1d.txt",
    "_Netherlands_valid.txt",
    "MegaCloud.txt",
    "OKcMix Valid.txt",
    "hotmail_Byy mega.txt",
    "Mix Good.txt",
    "UK_Bigg App for you my MEGA friends.txt",
    "BIG APP Mixed_ BY MEGACLOUD.txt",
    "number_pass Byy Mega.txt",
    "China_2_byy mega.txt",
    "JAPAN byy mega.txt",
    "GAMING GOOD.txt",
    "HOTMAIL MAILACCESS.txt",
    "VALID EU.txt",
    "09.01 EUROPE Valid.txt",
    "num_pass_MIX.txt",
    "HOTMAIL_fresh PART1.txt",
    "SOOOO VALID BYY MEGA.txt",
    "Germany million.txt",
    "Germany million part 2.txt",
    "Germany million part 3.txt",
    "G00D vALID.txt",
    "10k Goods_1 (1).txt",
    "10k Goods_2.txt",
    "10k Goods_3.txt",
    "hotmail_hq.txt",
    "hotmail_hq Part 2.txt",
    "Byyy mega.txt",
    "Mega_CORP_Combo.txt",
    "So G0d VAlid.txt",
    "Russian.txt",
    "SFR.FR HQ FRESH.txt",
]

def test_real_filenames():
    analyzer = FilenameAnalyzer()
    
    print("=" * 100)
    print("REAL FILENAMES ANALYSIS")
    print("=" * 100)
    
    database_count = 0
    combo_count = 0
    high_conf = 0
    med_conf = 0
    low_conf = 0
    
    print("\n[DATABASE DETECTIONS]")
    print("-" * 100)
    for filename in real_filenames:
        result = analyzer.analyze_filename(filename)
        
        if result.suggested_category == "Database":
            database_count += 1
            print(f"File: {filename:60} -> Database")
            print(f"      Domain: {result.domain_name or 'None':30} Conf: {result.confidence:6} | {result.reason}")
            
        if result.confidence == "high":
            high_conf += 1
        elif result.confidence == "medium":
            med_conf += 1
        else:
            low_conf += 1
    
    print("\n[COMBO DETECTIONS]")
    print("-" * 100)
    for filename in real_filenames:
        result = analyzer.analyze_filename(filename)
        
        if result.suggested_category == "Combo":
            combo_count += 1
    
    print(f"Total Combo files: {combo_count} (displaying count only, all others above are Database)")
    
    print("\n" + "=" * 100)
    print("STATISTICS")
    print("=" * 100)
    print(f"Total files:     {len(real_filenames)}")
    print(f"Database:        {database_count} ({database_count/len(real_filenames)*100:.1f}%)")
    print(f"Combo:           {combo_count} ({combo_count/len(real_filenames)*100:.1f}%)")
    print(f"\nConfidence levels:")
    print(f"High:            {high_conf} ({high_conf/len(real_filenames)*100:.1f}%)")
    print(f"Medium:          {med_conf} ({med_conf/len(real_filenames)*100:.1f}%)")
    print(f"Low:             {low_conf} ({low_conf/len(real_filenames)*100:.1f}%)")
    print("=" * 100)

if __name__ == "__main__":
    test_real_filenames()

