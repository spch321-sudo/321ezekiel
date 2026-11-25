# -*- coding: utf-8 -*-
import json
T={1:("Glory by the River Chebar","Open, See, Fall Down"),2:("Son of Man, Stand Up","Stand, Send, Eat"),3:("The Watchman and the Tongue Stuck to the Mouth","Eat, Watch, Mute"),
4:("The Picture of the Siege","Brick, Side, Bread"),5:("The Shaved Head and the Three Parts","Sword, Hair, Three"),6:("Prophesy to the Mountains","Mountains, Scatter, Know"),
7:("The End Has Come","End, Gold, Temple"),8:("The Dark Rooms in the Temple","Hand, Image, Sun"),9:("The Mark on the Forehead","Cry, Mark, Spare"),
10:("The Glory Leaves the Temple","Coals, Wheel, Out"),11:("A New Heart and the Glory Leaves the City","Pot, New, East"),12:("The Exile’s Baggage","Go, Sign, Near"),
13:("False Prophets and the Whitewashed Wall","Empty, Wall, Charm"),14:("Idols in the Heart","Heart, Inquire, Three"),15:("The Useless Vine","Vine, Fire, Waste"),
16:("The Abandoned Baby","Abandon, Beauty, Covenant"),17:("Two Great Eagles and the Tender Twig","Eagle, Covenant, Twig"),18:("The Soul Who Sins Shall Die","Proverb, Righteous, Return"),
19:("A Lament for the Lions","Lion, Pit, Branch"),20:("For My Name’s Sake","History, Name, Clean"),21:("The Sword Is Drawn","Sword, Fork, Crown"),
22:("Standing in the Gap","Blood, Dross, Breach"),23:("Two Sisters","Elder, Younger, Cup"),24:("The Pot and the Death of the Wife","Pot, Tears, Silent"),
25:("The Neighbors Who Gloat","Ammon, Moab, Philistia"),26:("The Walls of Tyre","Laugh, Waves, Deep"),27:("A Great Ship Sinking","Ship, Cargo, Sink"),
28:("The Pride of the King of Tyre","Pride, Garden, Fall"),29:("Egypt, the Great Crocodile in the River","Crocodile, Staff, Reward"),30:("The Day of Yahweh Is Near","Day, Break, Arm"),
31:("The Cedar of Lebanon","Cedar, Pride, Down"),32:("A Dirge for Egypt","Song, Pit, Sheol"),33:("The Watchman Sent Again","Watch, Return, Hear"),
34:("I Myself Will Be the Shepherd of My Sheep","Shepherd, Seek, Covenant"),35:("Mount Seir","Enmity, Waste, Hear"),36:("A New Heart and a New Spirit","Mountains, Name, New"),
37:("The Dry Bones Live","Bones, Breath, Join"),38:("The Coming of Gog","North, Gather, Show"),39:("The End of Gog and the Return","Fall, Bury, Return"),
40:("The Man with the Measuring Rod","Mountain, Man, Measure"),41:("The Inside of the Temple","Temple, Side, Holy"),42:("The Rooms of the Sanctuary","Rooms, Garments, Boundary"),
43:("The Glory Returns","East, Glory, Altar"),44:("Temple Order and the Priests","Gate, Servants, Portion"),45:("The Land Divided and the Feasts","Land, Prince, Feast"),
46:("The Prince and the People Worship","Gate, Prince, Kitchen"),47:("Water Flowing from the Temple Threshold","Water, Life, Border"),48:("Yahweh Is There","Tribes, City, Name")}
ARC={"呼召與榮耀的異象":"The Call and the Vision of Glory","圍困與結局":"Siege and End","殿中的穢行與榮耀離去":"Abominations in the Temple and the Departure of Glory",
"假盼望與個人的責任":"False Hope and Personal Responsibility","歷史的控訴與城的結局":"The Charge from History and the End of the City","列國":"The Nations",
"重生與盼望":"Renewal and Hope","新殿與榮耀歸回":"The New Temple and the Return of Glory"}
ISS={"ISS00_1":"Dating and the Prophet: What Is “the Thirtieth Year,” and What Kind of Prophet Is This?","ISS00_2":"The Vision and the Four Living Creatures: What Is Being Seen?",
"ISS00_3":"Personal Responsibility: Does “The Soul Who Sins Shall Die” Deny the Consequences for the Community?","ISS00_4":"Marriage and Sexual Imagery: What Are Chapters 16 and 23 Saying?",
"ISS00_5":"The King of Tyre and Satan: Who Is Chapter 28 About?","ISS00_6":"The Dry Bones: The Restoration of Israel, or the Resurrection of Persons?",
"ISS00_7":"Gog and Magog: Chapters 38–39—Who, and When?","ISS00_8":"The New Temple: Chapters 40–48—Literal, Symbolic, or Spiritual?"}
TR={"yada‘":"yada‘","kavod":"kavod","ruach":"ruach","lev":"lev","chayah":"chayah"}
if __name__=='__main__':
    b=json.load(open('blueprint.json')); arcs={c['arc'] for c in b['ch'].values()}
    assert arcs==set(ARC),arcs^set(ARC)
    ids=[i['id'] for i in b['issues']]; assert ids==list(ISS),ids
    json.dump({'t':{str(k):v[0] for k,v in T.items()},'sub':{str(k):v[1] for k,v in T.items()},'arc':ARC,'iss':ISS},open('en/canon.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print('ok')
