import os
import json
import re
from datetime import datetime

# The fonts we are collecting (Changed Files have a Zero-based index according to this list)
canvasFontList = [
    ".Aqua Kana",
    ".Helvetica LT MM",
    ".Times LT MM",
    "18thCentury",
    "8514oem",
    "AR BERKLEY",
    "AR JULIAN",
    "AR PL UKai CN",
    "AR PL UMing CN",
    "AR PL UMing HK",
    "AR PL UMing TW",
    "AR PL UMing TW MBE",
    "Aakar",
    "Abadi MT Condensed Extra Bold",
    "Abadi MT Condensed Light",
    "Abyssinica SIL",
    "AcmeFont",
    "Adobe Arabic",
    "Agency FB",
    "Aharoni",
    "Aharoni Bold",
    "Al Bayan",
    "Al Bayan Bold",
    "Al Bayan Plain",
    "Al Nile",
    "Al Tarikh",
    "Aldhabi",
    "Alfredo",
    "Algerian",
    "Alien Encounters",
    "Almonte Snow",
    "American Typewriter",
    "American Typewriter Bold",
    "American Typewriter Condensed",
    "American Typewriter Light",
    "Amethyst",
    "Andale Mono",
    "Andale Mono Version",
    "Andalus",
    "Angsana New",
    "AngsanaUPC",
    "Ani",
    "AnjaliOldLipi",
    "Aparajita",
    "Apple Braille",
    "Apple Braille Outline 6 Dot",
    "Apple Braille Outline 8 Dot",
    "Apple Braille Pinpoint 6 Dot",
    "Apple Braille Pinpoint 8 Dot",
    "Apple Chancery",
    "Apple Color Emoji",
    "Apple LiGothic Medium",
    "Apple LiSung Light",
    "Apple SD Gothic Neo",
    "Apple SD Gothic Neo Regular",
    "Apple SD GothicNeo ExtraBold",
    "Apple Symbols",
    "AppleGothic",
    "AppleGothic Regular",
    "AppleMyungjo",
    "AppleMyungjo Regular",
    "AquaKana",
    "Arabic Transparent",
    "Arabic Typesetting",
    "Arial",
    "Arial Baltic",
    "Arial Black",
    "Arial Bold",
    "Arial Bold Italic",
    "Arial CE",
    "Arial CYR",
    "Arial Greek",
    "Arial Hebrew",
    "Arial Hebrew Bold",
    "Arial Italic",
    "Arial Narrow",
    "Arial Narrow Bold",
    "Arial Narrow Bold Italic",
    "Arial Narrow Italic",
    "Arial Rounded Bold",
    "Arial Rounded MT Bold",
    "Arial TUR",
    "Arial Unicode MS",
    "ArialHB",
    "Arimo",
    "Asimov",
    "Autumn",
    "Avenir",
    "Avenir Black",
    "Avenir Book",
    "Avenir Next",
    "Avenir Next Bold",
    "Avenir Next Condensed",
    "Avenir Next Condensed Bold",
    "Avenir Next Demi Bold",
    "Avenir Next Heavy",
    "Avenir Next Regular",
    "Avenir Roman",
    "Ayuthaya",
    "BN Jinx",
    "BN Machine",
    "BOUTON International Symbols",
    "Baby Kruffy",
    "Baghdad",
    "Bahnschrift",
    "Balthazar",
    "Bangla MN",
    "Bangla MN Bold",
    "Bangla Sangam MN",
    "Bangla Sangam MN Bold",
    "Baskerville",
    "Baskerville Bold",
    "Baskerville Bold Italic",
    "Baskerville Old Face",
    "Baskerville SemiBold",
    "Baskerville SemiBold Italic",
    "Bastion",
    "Batang",
    "BatangChe",
    "Bauhaus 93",
    "Beirut",
    "Bell MT",
    "Bell MT Bold",
    "Bell MT Italic",
    "Bellerose",
    "Berlin Sans FB",
    "Berlin Sans FB Demi",
    "Bernard MT Condensed",
    "BiauKai",
    "Big Caslon",
    "Big Caslon Medium",
    "Birch Std",
    "Bitstream Charter",
    "Bitstream Vera Sans",
    "Blackadder ITC",
    "Blackoak Std",
    "Bobcat",
    "Bodoni 72",
    "Bodoni MT",
    "Bodoni MT Black",
    "Bodoni MT Poster Compressed",
    "Bodoni Ornaments",
    "BolsterBold",
    "Book Antiqua",
    "Book Antiqua Bold",
    "Bookman Old Style",
    "Bookman Old Style Bold",
    "Bookshelf Symbol 7",
    "Borealis",
    "Bradley Hand",
    "Bradley Hand ITC",
    "Braggadocio",
    "Brandish",
    "Britannic Bold",
    "Broadway",
    "Browallia New",
    "BrowalliaUPC",
    "Brush Script",
    "Brush Script MT",
    "Brush Script MT Italic",
    "Brush Script Std",
    "Brussels",
    "Calibri",
    "Calibri Bold",
    "Calibri Light",
    "Californian FB",
    "Calisto MT",
    "Calisto MT Bold",
    "Calligraphic",
    "Calvin",
    "Cambria",
    "Cambria Bold",
    "Cambria Math",
    "Candara",
    "Candara Bold",
    "Candles",
    "Carrois Gothic SC",
    "Castellar",
    "Centaur",
    "Century",
    "Century Gothic",
    "Century Gothic Bold",
    "Century Schoolbook",
    "Century Schoolbook Bold",
    "Century Schoolbook L",
    "Chalkboard",
    "Chalkboard Bold",
    "Chalkboard SE",
    "Chalkboard SE Bold",
    "ChalkboardBold",
    "Chalkduster",
    "Chandas",
    "Chaparral Pro",
    "Chaparral Pro Light",
    "Charlemagne Std",
    "Charter",
    "Chilanka",
    "Chiller",
    "Chinyen",
    "Clarendon",
    "Cochin",
    "Cochin Bold",
    "Colbert",
    "Colonna MT",
    "Comic Sans MS",
    "Comic Sans MS Bold",
    "Commons",
    "Consolas",
    "Consolas Bold",
    "Constantia",
    "Constantia Bold",
    "Coolsville",
    "Cooper Black",
    "Cooper Std Black",
    "Copperplate",
    "Copperplate Bold",
    "Copperplate Gothic Bold",
    "Copperplate Light",
    "Corbel",
    "Corbel Bold",
    "Cordia New",
    "CordiaUPC",
    "Corporate",
    "Corsiva",
    "Corsiva Hebrew",
    "Corsiva Hebrew Bold",
    "Courier",
    "Courier 10 Pitch",
    "Courier Bold",
    "Courier New",
    "Courier New Baltic",
    "Courier New Bold",
    "Courier New CE",
    "Courier New Italic",
    "Courier Oblique",
    "Cracked Johnnie",
    "Creepygirl",
    "Curlz MT",
    "Cursor",
    "Cutive Mono",
    "DFKai-SB",
    "DIN Alternate",
    "DIN Condensed",
    "Damascus",
    "Damascus Bold",
    "Dancing Script",
    "DaunPenh",
    "David",
    "Dayton",
    "DecoType Naskh",
    "Deja Vu",
    "DejaVu LGC Sans",
    "DejaVu Sans",
    "DejaVu Sans Mono",
    "DejaVu Serif",
    "Deneane",
    "Desdemona",
    "Detente",
    "Devanagari MT",
    "Devanagari MT Bold",
    "Devanagari Sangam MN",
    "Didot",
    "Didot Bold",
    "Digifit",
    "DilleniaUPC",
    "Dingbats",
    "Distant Galaxy",
    "Diwan Kufi",
    "Diwan Kufi Regular",
    "Diwan Thuluth",
    "Diwan Thuluth Regular",
    "DokChampa",
    "Dominican",
    "Dotum",
    "DotumChe",
    "Droid Sans",
    "Droid Sans Fallback",
    "Droid Sans Mono",
    "Dyuthi",
    "Ebrima",
    "Edwardian Script ITC",
    "Elephant",
    "Emmett",
    "Engravers MT",
    "Engravers MT Bold",
    "Enliven",
    "Eras Bold ITC",
    "Estrangelo Edessa",
    "Ethnocentric",
    "EucrosiaUPC",
    "Euphemia",
    "Euphemia UCAS",
    "Euphemia UCAS Bold",
    "Eurostile",
    "Eurostile Bold",
    "Expressway Rg",
    "FangSong",
    "Farah",
    "Farisi",
    "Felix Titling",
    "Fingerpop",
    "Fixedsys",
    "Flubber",
    "Footlight MT Light",
    "Forte",
    "FrankRuehl",
    "Frankfurter Venetian TT",
    "Franklin Gothic Book",
    "Franklin Gothic Book Italic",
    "Franklin Gothic Medium",
    "Franklin Gothic Medium Cond",
    "Franklin Gothic Medium Italic",
    "FreeMono",
    "FreeSans",
    "FreeSerif",
    "FreesiaUPC",
    "Freestyle Script",
    "French Script MT",
    "Futura",
    "Futura Condensed ExtraBold",
    "Futura Medium",
    "GB18030 Bitmap",
    "Gabriola",
    "Gadugi",
    "Garamond",
    "Garamond Bold",
    "Gargi",
    "Garuda",
    "Gautami",
    "Gazzarelli",
    "Geeza Pro",
    "Geeza Pro Bold",
    "Geneva",
    "GenevaCY",
    "Gentium",
    "Gentium Basic",
    "Gentium Book Basic",
    "GentiumAlt",
    "Georgia",
    "Georgia Bold",
    "Geotype TT",
    "Giddyup Std",
    "Gigi",
    "Gill",
    "Gill Sans",
    "Gill Sans Bold",
    "Gill Sans MT",
    "Gill Sans MT Bold",
    "Gill Sans MT Condensed",
    "Gill Sans MT Ext Condensed Bold",
    "Gill Sans MT Italic",
    "Gill Sans Ultra Bold",
    "Gill Sans Ultra Bold Condensed",
    "Gisha",
    "Glockenspiel",
    "Gloucester MT Extra Condensed",
    "Good Times",
    "Goudy",
    "Goudy Old Style",
    "Goudy Old Style Bold",
    "Goudy Stout",
    "Greek Diner Inline TT",
    "Gubbi",
    "Gujarati MT",
    "Gujarati MT Bold",
    "Gujarati Sangam MN",
    "Gujarati Sangam MN Bold",
    "Gulim",
    "GulimChe",
    "GungSeo Regular",
    "Gungseouche",
    "Gungsuh",
    "GungsuhChe",
    "Gurmukhi",
    "Gurmukhi MN",
    "Gurmukhi MN Bold",
    "Gurmukhi MT",
    "Gurmukhi Sangam MN",
    "Gurmukhi Sangam MN Bold",
    "Haettenschweiler",
    "Hand Me Down S (BRK)",
    "Hansen",
    "Harlow Solid Italic",
    "Harrington",
    "Harvest",
    "HarvestItal",
    "Haxton Logos TT",
    "HeadLineA Regular",
    "HeadlineA",
    "Heavy Heap",
    "Hei",
    "Hei Regular",
    "Heiti SC",
    "Heiti SC Light",
    "Heiti SC Medium",
    "Heiti TC",
    "Heiti TC Light",
    "Heiti TC Medium",
    "Helvetica",
    "Helvetica Bold",
    "Helvetica CY Bold",
    "Helvetica CY Plain",
    "Helvetica LT Std",
    "Helvetica Light",
    "Helvetica Neue",
    "Helvetica Neue Bold",
    "Helvetica Neue Medium",
    "Helvetica Oblique",
    "HelveticaCY",
    "HelveticaNeueLT Com 107 XBlkCn",
    "Herculanum",
    "High Tower Text",
    "Highboot",
    "Hiragino Kaku Gothic Pro W3",
    "Hiragino Kaku Gothic Pro W6",
    "Hiragino Kaku Gothic ProN W3",
    "Hiragino Kaku Gothic ProN W6",
    "Hiragino Kaku Gothic Std W8",
    "Hiragino Kaku Gothic StdN W8",
    "Hiragino Maru Gothic Pro W4",
    "Hiragino Maru Gothic ProN W4",
    "Hiragino Mincho Pro W3",
    "Hiragino Mincho Pro W6",
    "Hiragino Mincho ProN W3",
    "Hiragino Mincho ProN W6",
    "Hiragino Sans GB W3",
    "Hiragino Sans GB W6",
    "Hiragino Sans W0",
    "Hiragino Sans W1",
    "Hiragino Sans W2",
    "Hiragino Sans W3",
    "Hiragino Sans W4",
    "Hiragino Sans W5",
    "Hiragino Sans W6",
    "Hiragino Sans W7",
    "Hiragino Sans W8",
    "Hiragino Sans W9",
    "Hobo Std",
    "Hoefler Text",
    "Hoefler Text Black",
    "Hoefler Text Ornaments",
    "Hollywood Hills",
    "Hombre",
    "Huxley Titling",
    "ITC Stone Serif",
    "ITF Devanagari",
    "ITF Devanagari Marathi",
    "ITF Devanagari Medium",
    "Impact",
    "Imprint MT Shadow",
    "InaiMathi",
    "Induction",
    "Informal Roman",
    "Ink Free",
    "IrisUPC",
    "Iskoola Pota",
    "Italianate",
    "Jamrul",
    "JasmineUPC",
    "Javanese Text",
    "Jokerman",
    "Juice ITC",
    "KacstArt",
    "KacstBook",
    "KacstDecorative",
    "KacstDigital",
    "KacstFarsi",
    "KacstLetter",
    "KacstNaskh",
    "KacstOffice",
    "KacstOne",
    "KacstPen",
    "KacstPoster",
    "KacstQurn",
    "KacstScreen",
    "KacstTitle",
    "KacstTitleL",
    "Kai",
    "Kai Regular",
    "KaiTi",
    "Kailasa",
    "Kailasa Regular",
    "Kaiti SC",
    "Kaiti SC Black",
    "Kalapi",
    "Kalimati",
    "Kalinga",
    "Kannada MN",
    "Kannada MN Bold",
    "Kannada Sangam MN",
    "Kannada Sangam MN Bold",
    "Kartika",
    "Karumbi",
    "Kedage",
    "Kefa",
    "Kefa Bold",
    "Keraleeyam",
    "Keyboard",
    "Khmer MN",
    "Khmer MN Bold",
    "Khmer OS",
    "Khmer OS System",
    "Khmer Sangam MN",
    "Khmer UI",
    "Kinnari",
    "Kino MT",
    "KodchiangUPC",
    "Kohinoor Bangla",
    "Kohinoor Devanagari",
    "Kohinoor Telugu",
    "Kokila",
    "Kokonor",
    "Kokonor Regular",
    "Kozuka Gothic Pr6N B",
    "Kristen ITC",
    "Krungthep",
    "KufiStandardGK",
    "KufiStandardGK Regular",
    "Kunstler Script",
    "Laksaman",
    "Lao MN",
    "Lao Sangam MN",
    "Lao UI",
    "LastResort",
    "Latha",
    "Leelawadee",
    "Letter Gothic Std",
    "LetterOMatic!",
    "Levenim MT",
    "LiHei Pro",
    "LiSong Pro",
    "Liberation Mono",
    "Liberation Sans",
    "Liberation Sans Narrow",
    "Liberation Serif",
    "Likhan",
    "LilyUPC",
    "Limousine",
    "Lithos Pro Regular",
    "LittleLordFontleroy",
    "Lohit Assamese",
    "Lohit Bengali",
    "Lohit Devanagari",
    "Lohit Gujarati",
    "Lohit Gurmukhi",
    "Lohit Hindi",
    "Lohit Kannada",
    "Lohit Malayalam",
    "Lohit Odia",
    "Lohit Punjabi",
    "Lohit Tamil",
    "Lohit Tamil Classical",
    "Lohit Telugu",
    "Loma",
    "Lucida Blackletter",
    "Lucida Bright",
    "Lucida Bright Demibold",
    "Lucida Bright Demibold Italic",
    "Lucida Bright Italic",
    "Lucida Calligraphy",
    "Lucida Calligraphy Italic",
    "Lucida Console",
    "Lucida Fax",
    "Lucida Fax Demibold",
    "Lucida Fax Regular",
    "Lucida Grande",
    "Lucida Grande Bold",
    "Lucida Handwriting",
    "Lucida Handwriting Italic",
    "Lucida Sans",
    "Lucida Sans Demibold Italic",
    "Lucida Sans Typewriter",
    "Lucida Sans Typewriter Bold",
    "Lucida Sans Unicode",
    "Luminari",
    "Luxi Mono",
    "MS Gothic",
    "MS Mincho",
    "MS Outlook",
    "MS PGothic",
    "MS PMincho",
    "MS Reference Sans Serif",
    "MS Reference Specialty",
    "MS Sans Serif",
    "MS Serif",
    "MS UI Gothic",
    "MT Extra",
    "MV Boli",
    "Mael",
    "Magneto",
    "Maiandra GD",
    "Malayalam MN",
    "Malayalam MN Bold",
    "Malayalam Sangam MN",
    "Malayalam Sangam MN Bold",
    "Malgun Gothic",
    "Mallige",
    "Mangal",
    "Manorly",
    "Marion",
    "Marion Bold",
    "Marker Felt",
    "Marker Felt Thin",
    "Marlett",
    "Martina",
    "Matura MT Script Capitals",
    "Meera",
    "Meiryo",
    "Meiryo Bold",
    "Meiryo UI",
    "MelodBold",
    "Menlo",
    "Menlo Bold",
    "Mesquite Std",
    "Microsoft",
    "Microsoft Himalaya",
    "Microsoft JhengHei",
    "Microsoft JhengHei UI",
    "Microsoft New Tai Lue",
    "Microsoft PhagsPa",
    "Microsoft Sans Serif",
    "Microsoft Tai Le",
    "Microsoft Tai Le Bold",
    "Microsoft Uighur",
    "Microsoft YaHei",
    "Microsoft YaHei UI",
    "Microsoft Yi Baiti",
    "Minerva",
    "MingLiU",
    "MingLiU-ExtB",
    "MingLiU_HKSCS",
    "Minion Pro",
    "Miriam",
    "Mishafi",
    "Mishafi Gold",
    "Mistral",
    "Modern",
    "Modern No. 20",
    "Monaco",
    "Mongolian Baiti",
    "Monospace",
    "Monotype Corsiva",
    "Monotype Sorts",
    "MoolBoran",
    "Moonbeam",
    "MotoyaLMaru",
    "Mshtakan",
    "Mshtakan Bold",
    "Mukti Narrow",
    "Muna",
    "Myanmar MN",
    "Myanmar MN Bold",
    "Myanmar Sangam MN",
    "Myanmar Text",
    "Mycalc",
    "Myriad Arabic",
    "Myriad Hebrew",
    "Myriad Pro",
    "NISC18030",
    "NSimSun",
    "Nadeem",
    "Nadeem Regular",
    "Nakula",
    "Nanum Barun Gothic",
    "Nanum Gothic",
    "Nanum Myeongjo",
    "NanumBarunGothic",
    "NanumGothic",
    "NanumGothic Bold",
    "NanumGothicCoding",
    "NanumMyeongjo",
    "NanumMyeongjo Bold",
    "Narkisim",
    "Nasalization",
    "Navilu",
    "Neon Lights",
    "New Peninim MT",
    "New Peninim MT Bold",
    "News Gothic MT",
    "News Gothic MT Bold",
    "Niagara Engraved",
    "Niagara Solid",
    "Nimbus Mono L",
    "Nimbus Roman No9 L",
    "Nimbus Sans L",
    "Nimbus Sans L Condensed",
    "Nina",
    "Nirmala UI",
    "Nirmala.ttf",
    "Norasi",
    "Noteworthy",
    "Noteworthy Bold",
    "Noto Color Emoji",
    "Noto Emoji",
    "Noto Mono",
    "Noto Naskh Arabic",
    "Noto Nastaliq Urdu",
    "Noto Sans",
    "Noto Sans Armenian",
    "Noto Sans Bengali",
    "Noto Sans CJK",
    "Noto Sans Canadian Aboriginal",
    "Noto Sans Cherokee",
    "Noto Sans Devanagari",
    "Noto Sans Ethiopic",
    "Noto Sans Georgian",
    "Noto Sans Gujarati",
    "Noto Sans Gurmukhi",
    "Noto Sans Hebrew",
    "Noto Sans JP",
    "Noto Sans KR",
    "Noto Sans Kannada",
    "Noto Sans Khmer",
    "Noto Sans Lao",
    "Noto Sans Malayalam",
    "Noto Sans Myanmar",
    "Noto Sans Oriya",
    "Noto Sans SC",
    "Noto Sans Sinhala",
    "Noto Sans Symbols",
    "Noto Sans TC",
    "Noto Sans Tamil",
    "Noto Sans Telugu",
    "Noto Sans Thai",
    "Noto Sans Yi",
    "Noto Serif",
    "Notram",
    "November",
    "Nueva Std",
    "Nueva Std Cond",
    "Nyala",
    "OCR A Extended",
    "OCR A Std",
    "Old English Text MT",
    "OldeEnglish",
    "Onyx",
    "OpenSymbol",
    "OpineHeavy",
    "Optima",
    "Optima Bold",
    "Optima Regular",
    "Orator Std",
    "Oriya MN",
    "Oriya MN Bold",
    "Oriya Sangam MN",
    "Oriya Sangam MN Bold",
    "Osaka",
    "Osaka-Mono",
    "OsakaMono",
    "PCMyungjo Regular",
    "PCmyoungjo",
    "PMingLiU",
    "PMingLiU-ExtB",
    "PR Celtic Narrow",
    "PT Mono",
    "PT Sans",
    "PT Sans Bold",
    "PT Sans Caption Bold",
    "PT Sans Narrow Bold",
    "PT Serif",
    "Padauk",
    "Padauk Book",
    "Padmaa",
    "Pagul",
    "Palace Script MT",
    "Palatino",
    "Palatino Bold",
    "Palatino Linotype",
    "Palatino Linotype Bold",
    "Papyrus",
    "Papyrus Condensed",
    "Parchment",
    "Parry Hotter",
    "PenultimateLight",
    "Perpetua",
    "Perpetua Bold",
    "Perpetua Titling MT",
    "Perpetua Titling MT Bold",
    "Phetsarath OT",
    "Phosphate",
    "Phosphate Inline",
    "Phosphate Solid",
    "PhrasticMedium",
    "PilGi Regular",
    "Pilgiche",
    "PingFang HK",
    "PingFang SC",
    "PingFang TC",
    "Pirate",
    "Plantagenet Cherokee",
    "Playbill",
    "Poor Richard",
    "Poplar Std",
    "Pothana2000",
    "Prestige Elite Std",
    "Pristina",
    "Purisa",
    "QuiverItal",
    "Raanana",
    "Raanana Bold",
    "Raavi",
    "Rachana",
    "Rage Italic",
    "RaghuMalayalam",
    "Ravie",
    "Rekha",
    "Roboto",
    "Rockwell",
    "Rockwell Bold",
    "Rockwell Condensed",
    "Rockwell Extra Bold",
    "Rockwell Italic",
    "Rod",
    "Roland",
    "Rondalo",
    "Rosewood Std Regular",
    "RowdyHeavy",
    "Russel Write TT",
    "SF Movie Poster",
    "STFangsong",
    "STHeiti",
    "STIXGeneral",
    "STIXGeneral-Bold",
    "STIXGeneral-Regular",
    "STIXIntegralsD",
    "STIXIntegralsD-Bold",
    "STIXIntegralsSm",
    "STIXIntegralsSm-Bold",
    "STIXIntegralsUp",
    "STIXIntegralsUp-Bold",
    "STIXIntegralsUp-Regular",
    "STIXIntegralsUpD",
    "STIXIntegralsUpD-Bold",
    "STIXIntegralsUpD-Regular",
    "STIXIntegralsUpSm",
    "STIXIntegralsUpSm-Bold",
    "STIXNonUnicode",
    "STIXNonUnicode-Bold",
    "STIXSizeFiveSym",
    "STIXSizeFiveSym-Regular",
    "STIXSizeFourSym",
    "STIXSizeFourSym-Bold",
    "STIXSizeOneSym",
    "STIXSizeOneSym-Bold",
    "STIXSizeThreeSym",
    "STIXSizeThreeSym-Bold",
    "STIXSizeTwoSym",
    "STIXSizeTwoSym-Bold",
    "STIXVariants",
    "STIXVariants-Bold",
    "STKaiti",
    "STSong",
    "STXihei",
    "SWGamekeys MT",
    "Saab",
    "Sahadeva",
    "Sakkal Majalla",
    "Salina",
    "Samanata",
    "Samyak Devanagari",
    "Samyak Gujarati",
    "Samyak Malayalam",
    "Samyak Tamil",
    "Sana",
    "Sana Regular",
    "Sans",
    "Sarai",
    "Sathu",
    "Savoye LET Plain:1.0",
    "Sawasdee",
    "Script",
    "Script MT Bold",
    "Segoe MDL2 Assets",
    "Segoe Print",
    "Segoe Pseudo",
    "Segoe Script",
    "Segoe UI",
    "Segoe UI Emoji",
    "Segoe UI Historic",
    "Segoe UI Semilight",
    "Segoe UI Symbol",
    "Serif",
    "Shonar Bangla",
    "Showcard Gothic",
    "Shree Devanagari 714",
    "Shruti",
    "SignPainter-HouseScript",
    "Silom",
    "SimHei",
    "SimSun",
    "SimSun-ExtB",
    "Simplified Arabic",
    "Simplified Arabic Fixed",
    "Sinhala MN",
    "Sinhala MN Bold",
    "Sinhala Sangam MN",
    "Sinhala Sangam MN Bold",
    "Sitka",
    "Skia",
    "Skia Regular",
    "Skinny",
    "Small Fonts",
    "Snap ITC",
    "Snell Roundhand",
    "Snowdrift",
    "Songti SC",
    "Songti SC Black",
    "Songti TC",
    "Source Code Pro",
    "Splash",
    "Standard Symbols L",
    "Stencil",
    "Stencil Std",
    "Stephen",
    "Sukhumvit Set",
    "Suruma",
    "Sylfaen",
    "Symbol",
    "Symbole",
    "System",
    "System Font",
    "TAMu_Kadambri",
    "TAMu_Kalyani",
    "TAMu_Maduram",
    "TSCu_Comic",
    "TSCu_Paranar",
    "TSCu_Times",
    "Tahoma",
    "Tahoma Negreta",
    "TakaoExGothic",
    "TakaoExMincho",
    "TakaoGothic",
    "TakaoMincho",
    "TakaoPGothic",
    "TakaoPMincho",
    "Tamil MN",
    "Tamil MN Bold",
    "Tamil Sangam MN",
    "Tamil Sangam MN Bold",
    "Tarzan",
    "Tekton Pro",
    "Tekton Pro Cond",
    "Tekton Pro Ext",
    "Telugu MN",
    "Telugu MN Bold",
    "Telugu Sangam MN",
    "Telugu Sangam MN Bold",
    "Tempus Sans ITC",
    "Terminal",
    "Terminator Two",
    "Thonburi",
    "Thonburi Bold",
    "Tibetan Machine Uni",
    "Times",
    "Times Bold",
    "Times New Roman",
    "Times New Roman Baltic",
    "Times New Roman Bold",
    "Times New Roman Italic",
    "Times Roman",
    "Tlwg Mono",
    "Tlwg Typewriter",
    "Tlwg Typist",
    "Tlwg Typo",
    "TlwgMono",
    "TlwgTypewriter",
    "Toledo",
    "Traditional Arabic",
    "Trajan Pro",
    "Trattatello",
    "Trebuchet MS",
    "Trebuchet MS Bold",
    "Tunga",
    "Tw Cen MT",
    "Tw Cen MT Bold",
    "Tw Cen MT Italic",
    "URW Bookman L",
    "URW Chancery L",
    "URW Gothic L",
    "URW Palladio L",
    "Ubuntu",
    "Ubuntu Condensed",
    "Ubuntu Mono",
    "Ukai",
    "Ume Gothic",
    "Ume Mincho",
    "Ume P Gothic",
    "Ume P Mincho",
    "Ume UI Gothic",
    "Uming",
    "Umpush",
    "UnBatang",
    "UnDinaru",
    "UnDotum",
    "UnGraphic",
    "UnGungseo",
    "UnPilgi",
    "Untitled1",
    "Urdu Typesetting",
    "Uroob",
    "Utkal",
    "Utopia",
    "Utsaah",
    "Valken",
    "Vani",
    "Vemana2000",
    "Verdana",
    "Verdana Bold",
    "Vijaya",
    "Viner Hand ITC",
    "Vivaldi",
    "Vivian",
    "Vladimir Script",
    "Vrinda",
    "Waree",
    "Waseem",
    "Waverly",
    "Webdings",
    "WenQuanYi Bitmap Song",
    "WenQuanYi Micro Hei",
    "WenQuanYi Micro Hei Mono",
    "WenQuanYi Zen Hei",
    "Whimsy TT",
    "Wide Latin",
    "Wingdings",
    "Wingdings 2",
    "Wingdings 3",
    "Woodcut",
    "X-Files",
    "Year supply of fairy cakes",
    "Yu Gothic",
    "Yu Mincho",
    "Yuppy SC",
    "Yuppy SC Regular",
    "Yuppy TC",
    "Yuppy TC Regular",
    "Zapf Dingbats",
    "Zapfino",
    "Zawgyi-One",
    "gargi",
    "lklug",
    "mry_KacstQurn",
    "ori1Uni",
    "DejaVu Serif Condensed",
    "Droid Serif",
    "sans-serif-thin",
    "ARNO PRO",
    "AvantGarde Bk BT",
    "BankGothic Md BT",
    "Bitstream Vera Sans Mono",
    "EUROSTILE",
    "Franklin Gothic",
    "Futura Bk BT",
    "Futura Md BT",
    "GOTHAM",
    "HELV",
    "Humanst521 BT",
    "Letter Gothic",
    "MYRIAD PRO",
    "SCRIPTINA",
    "Segoe UI Light",
    "Serifa",
    "Staccato222 BT",
    "TRAJAN PRO",
    "Univers CE 55 Medium",
    "ZWAdobeF",
    "monospace",
    "sans-serif",
    "serif"
]

fpElements = ['fingerprintJS', 'complexCanvas', 'canvasFonts', 'screen']

# UserAgents

# Windows/Chrome
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_125_0_0_0_Safari_537_36_'
# Windows/Firefox
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__rv_125_0__Gecko_20100101_Firefox_125_0_'
# Windows/Edge
# userAgent = 'Mozilla_5_0__Windows_NT_10_0__Win64__x64__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_125_0_0_0_Safari_537_36_Edg_125_0_0_0_'
# Mac/Safari
# userAgent = 'Mozilla_5_0__Macintosh__Intel_Mac_OS_X_10_15_7__AppleWebKit_605_1_15__KHTML__like_Gecko__Version_17_5_Safari_605_1_15_'
# Mac/Chrome
# userAgent = 'Mozilla_5_0__Macintosh__Intel_Mac_OS_X_10_15_7__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_125_0_0_0_Safari_537_36_'
# Mac/Firefox
# userAgent = 'Mozilla_5_0__Macintosh__Intel_Mac_OS_X_10_15__rv_126_0__Gecko_20100101_Firefox_126_0_'
# Android/Chrome
userAgent = 'Mozilla_5_0__Linux__Android_10__K__AppleWebKit_537_36__KHTML__like_Gecko__Chrome_125_0_0_0_Mobile_Safari_537_36_'

# Dir Path to search
path = '/home/xu/f5/fpCollector/json'

# File Limit
fileLimit = 100000


# Define a function to extract the date and time from the file name
def extractDateTime(file_name):
    match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})', file_name)
    if match:
        return datetime.strptime(match.group(), '%Y-%m-%dT%H-%M-%S')
    else:
        return datetime.min  # Default value if date is not found 

# Function to recursively search for "original" and "new" values
def find_original_and_new(obj):
    if isinstance(obj, dict):
        if 'original' in obj:
            return obj['original'], obj.get('new')
        for value in obj.values():
            original, new = find_original_and_new(value)
            if original is not None:
                return original, new
    elif isinstance(obj, list):
        for item in obj:
            original, new = find_original_and_new(item)
            if original is not None:
                return original, new
    return None, None

# get the first 10000 files from a list matching a userAgent (Minus the base)
def getAllFiles(dir, userAgent, isChrome):
    matching = []
    limit = 1
    try:
        # Get all files with useragent
        for root, dirs, files, in os.walk(dir):
            for file in files:
                filePath = os.path.join(root, file)
                if os.path.isfile(filePath):
                    if isChrome:
                        if userAgent in file and 'base' not in file and limit <= fileLimit and 'Edg' not in file:
                            matching.append(filePath)
                            limit = limit + 1
                    else:
                        if userAgent in file and 'base' not in file and limit <= fileLimit:
                            matching.append(filePath)
                            limit = limit + 1
    except Exception as e:
        print(f"Error: {e}")
    return matching

# count how many times the file size changed
def getChangedFiles(files):
    prevFileSize = None
    changes = []
    for file in files:
        if prevFileSize is not None and os.path.getsize(file) != prevFileSize:
            # print(file)
            changes.append(file)
        prevFileSize = os.path.getsize(file)

    return changes  

# get the fonts that are changing in the files
def getFonts(files):
    originalLen = 0

    baseFonts = {}
    newFonts = {}
    testFonts = set(f5Fonts)
    uniqueOriginal = set()
    uniqueNew = set()
    uniqueFontLists = set()
    results = {}
    for file in files:
        try:
            # Load file
            with open(file) as json_file:
                data = json.load(json_file)
            # Check if the fonts are in the file (They changed)
            if 'components' in data and 'fonts' in data['components'] and 'value' in data['components']['fonts']:
                # Get the fonts
                for fontId, fontData in data['components']['fonts']['value'].items():
                    if "original" in fontData:
                        baseFonts[fontData["original"]] = baseFonts.get(fontData["original"], 0) + 1
                        uniqueOriginal.add(fontData["original"])
                    if "new" in fontData:
                        uniqueNew.add(fontData["new"])
                        newFonts[fontData["new"]] = newFonts.get(fontData["new"], 0) + 1
                # compare the fonts of current file, and log them
                uniqueChanged = uniqueNew ^ uniqueOriginal
                if (len(uniqueOriginal) > originalLen):
                    originalLen = len(uniqueOriginal)
                frozenUnique = frozenset(uniqueNew)
                frozenOriginal = frozenset(uniqueOriginal)
                uniqueFontLists.add(frozenUnique)
                uniqueFontLists.add(frozenOriginal)
                for font in uniqueChanged:
                    results[font] = results.get(font, 0) + 1
                # clear the sets for the next file
                uniqueNew.clear()
                uniqueOriginal.clear()
                uniqueChanged.clear()

        except Exception as e:
            print(file)
            print(f"Error: {e}")
    sorted_dict = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    return originalLen

def getUniqueValues(files):
    uniques = {}
    for file in files:
        if not os.path.exists(file):
            print("File not found")
            continue
        try:
            with open(file, 'r') as jsonFile:
                data = json.load(jsonFile)
        except json.JSONDecodeError:
            print(f"Error decoding file ${file}")
            continue
        if "components" in data:
            components = data.get("components", {})
            for component, value in components.items():
                original, new = find_original_and_new(value)
                uniques.setdefault(component, set()).add(original)
                uniques.setdefault(component, set()).add(new)

                
    return uniques

def getUniqueVisitorIds(files):
    uniques = set()
    for file in files:
        if not os.path.exists(file):
            print("File not found")
            continue
        try:
            with open(file, 'r') as jsonFile:
                data = json.load(jsonFile)
        except json.JSONDecodeError:
            print(f"Error decoding file ${file}")
            continue
        if "visitorId" in data:
            uniques.add(data["visitorId"]["original"])
            uniques.add(data["visitorId"]["new"])


                
    return uniques

# Takes changed files and counts what fp vector is changing
def getTopics(files):
    changes = {}
    for file in files:
        if not os.path.exists(file):
            print("File not found")
            continue
        try:
            with open(file, 'r') as jsonFile:
                data = json.load(jsonFile)
        except json.JSONDecodeError:
            print(f"Error decoding file ${file}")
            continue
        # see what attributes are changing
        for element in fpElements:
            if element in data:
                if element in changes:
                    changes[element] += 1
                else:
                    changes[element] = 1
                    print(element, file)
    return changes

# Takes all files and counts what fonts are changing
def getCanvasFontChanges(files):
    changes = {}
    previousIds = set()
    changedIds = set()
    currentIds = set()
    for file in files:
        if not os.path.exists(file):
            print("File not found")
            continue
        try:
            with open(file, 'r') as jsonFile:
                data = json.load(jsonFile)
        except json.JSONDecodeError:
            print(f"Error decoding file ${file}")
            continue
        # check for canvasFonts in current file
        if 'canvasFonts' in data:
            # get the current font ids
            currentIds = set(data.get("canvasFonts", {}).get("fonts", {}).keys())
            # get what changed (if anything at all)
            changedIds = previousIds ^ currentIds
            # add them to the changes
            for fontId in changedIds:
                changes[fontId] = changes.get(fontId, 0) + 1
        # The current file doesnt have canvasFonts
        else:
            # add all previousIds to changes
            for fontId in previousIds:
                changes[fontId] = changes.get(fontId, 0) + 1
        previousIds = currentIds
        changedIds.clear()
        currentIds.clear()

    return changes

# Takes font dictionary from canvasFontChanges and converts the keys to the corresponding font
def getNamedFontChanges(changes):
    results = {}
    for font in changes.keys():
        index = int(font)
        results[canvasFontList[index]] = changes[font]
    return results

# Takes files and gets the components of fingerprintJS that are changing
def getFingerprintChanges(files):
    changes = {}
    tally = 0
    prev = False
    for file in files:
        if not os.path.exists(file):
            print("File not found")
            continue
        try:
            with open(file, 'r') as jsonFile:
                data = json.load(jsonFile)
        except json.JSONDecodeError:
            print(f"Error decoding file ${file}")
            continue
        if 'fingerprintJS' in data:
            if not prev:
                tally += 1
                prev = True
                print(file)
            # iterate through components and get attributes
            fingerprint_data = data.get('fingerprintJS', {})
            components = fingerprint_data.get('components', {})
            for value in components.keys():
                if value in changes:
                    changes[value] += 1
                    # print(value, file)
                else:
                    # print(value, file)
                    changes[value] = 1
        else:
            prev = False
    print("Number of changes in FingerprintJS: ", tally)
    return changes

# Get the canvas changes in files
def getCanvasChanges(files):
    changes = {}
    for file in files:
        if not os.path.exists(file):
            print("File not found")
            continue
        try:
            with open(file, 'r') as jsonFile:
                data = json.load(jsonFile)
        except json.JSONDecodeError:
            print(f"Error decoding file ${file}")
            continue
        if 'complexCanvas' in data:
            print(file)
    return changes

# gets number of changes for userAgent
def findNumChanges():
    files = getAllFiles(path, userAgent, False)
    sortedFiles = sorted(files, key=extractDateTime)
    changedFiles = getChangedFiles(sortedFiles)
    print("UserAgent: ", userAgent)
    print("Files sorted: ", len(sortedFiles))
    print("Number of changes: ", len(changedFiles))
    print("Vectors changed: ", getTopics(sortedFiles)) 
    # fontChanges = getCanvasFontChanges(sortedFiles)
    # print("Fonts changed: ", getNamedFontChanges(fontChanges))
    # print("FingerprintJS Changes: ", getFingerprintChanges(sortedFiles))
    # print("Complex Canvas Changes: ", getCanvasChanges(sortedFiles))
findNumChanges()