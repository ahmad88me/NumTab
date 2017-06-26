import json

'''
The example output file that is analysed by this code is presented at the end
of this file
'''

data = []

# function filling data object with data from result.json file
# results.json file is an output file of MSL approach
def formatObjects(dataFile):
    print dataFile
    oneObject = ""
    filePath  = ""
    with open(dataFile) as f:
        for line in f:
            line = line.strip( '\n')
            if './'in line:
                filePath = line
            if line == '{':
                oneObject = line
            elif line == '}':
                oneObject = oneObject + line
                o = json.loads(oneObject)
                o["file"] = filePath
                data.append(o)
            else:
                oneObject = oneObject + line
    print len(data)


# function used to calculate MRR scores for MSL approach
# not used to compare with DSL because of the differences in
# outputs of both of the approaches
def calculateMRR():
    majMRR = 0.00
    avgMRR = 0.00
    for o in data:
        fileName = o['file']
        fileName = fileName.split('+')
        fileName = fileName[5]
        fileName = fileName.split('.')
        fileName = fileName[0]

        avg = o['labelling']['property']['avg']
        maj = o['labelling']['property']['maj']

        counter = 0
        correctLabelPossition = 0
        for label in avg:
            counter += 1
            if label[0] == fileName:
                correctLabelPossition = counter

        if correctLabelPossition > 0:
            majMRR += (1/correctLabelPossition)

        counter = 0
        correctLabelPossition = 0
        for label in maj:
            counter += 1
            if label[0] == fileName:
                correctLabelPossition = counter

        if correctLabelPossition > 0:
            avgMRR += (1/correctLabelPossition)
    majMRR = majMRR/len(data)
    avgMRR = avgMRR/len(data)
    print "MRR results: "
    print majMRR
    print avgMRR

# function used to calculate modified MRR scores for MSL approach
# used to compare with DSL approach
# assuming the same relevance for each three labels
def calculateKarmaMRR():
    majMRR = 0.00
    avgMRR = 0.00
    for o in data:
        fileName = o['file']
        fileName = fileName.split('+')
        fileName = fileName[7]
        #fileName = fileName[5]
        #fileName = fileName.split('.')
        #fileName = fileName[0]
        avg = o['labelling']['property']['avg']
        maj = o['labelling']['property']['maj']

        counter = 0
        correctLabelPossition = 0
        for label in avg:
            counter += 1
            if label[0] == fileName:
                correctLabelPossition = counter
        if correctLabelPossition > 0:
            if correctLabelPossition <= 3:
                majMRR += (1/1)
            elif correctLabelPossition <= 6:
                majMRR += (1/2)
            elif correctLabelPossition <= 9:
                majMRR += (1/3)
            elif correctLabelPossition <= 12:
                majMRR += (1/4)
        counter = 0
        correctLabelPossition = 0
        for label in maj:
            counter += 1
            if label[0] == fileName:
                correctLabelPossition = counter
        if correctLabelPossition > 0:
            if correctLabelPossition <= 3:
                avgMRR += (1/1)
            elif correctLabelPossition <= 6:
                avgMRR += (1/2)
            elif correctLabelPossition <= 9:
                avgMRR += (1/3)
            elif correctLabelPossition <= 12:
                avgMRR += (1/4)
    majMRR = majMRR/len(data)
    avgMRR = avgMRR/len(data)
    print "MRR results: "
    print majMRR
    print avgMRR


# function calculating the results of MSL approach to the same
# structure as presented by authors in their study
def printEval():
    top_k = [1, 5, 10]
    scores = {}
    scores["maj"] = {}
    scores['avg'] = {}
    for k in top_k:
        scores["maj"][k] = 0
        scores['avg'][k] = 0
        counter = 0
        for o in data:
            counter += 1
            #fileName = o['file'].split('"')
            fileName = o['file']
            fileName = fileName.split('+')

            fileName = fileName[7]
            #fileName = fileName.split('.')
            #fileName = fileName[0]

            avg = o['labelling']['property']['avg']
            maj = o['labelling']['property']['maj']

            # avg function scores
            i = 1
            flag = False
            for label in avg:

                if label[0] == fileName:
                    flag = True
                if i == k:
                    break
                i += 1
            if flag:
                scores["avg"][k] += 1

            # maj function scores
            i = 1
            flag = False
            for label in maj:
                if label[0] == fileName:
                    flag = True
                if i == k:
                    break
                i += 1
            if flag:
                scores["maj"][k] += 1
        scores['counter'] = counter
    print scores
    return scores

# function used to print scores of MSL approach
def getStats(scores):
    print "maj:"
    for k in scores['maj']:
        val = round(float(scores['maj'][k])/float(scores['counter']) * 100, 1)
        print str(k)+ " " + str(val)
    print "avg:"
    for k in scores['avg']:
        val = round(float(scores['avg'][k])/float(scores['counter']) * 100, 1)
        print str(k)+ " " + str(val)

#formatFile()
formatObjects('results.json')
scores = printEval()
getStats(scores)
calculateKarmaMRR()


'''
Below we provide a sample output of MSL approach for bag of values
disambiguated to property "assets" saved to results.json file

{
"file": "./71906453_0_7287774935077400431.csv+3+http:++dbpedia.org+ontology+assets.csv",
  "invalid": [],
  "labelling": {
    "property": {
      "avg": [
        [
          "populationDensity",
          0.3125
        ],
        [
          "minimumElevation",
          0.315
        ],
        [
          "number",
          0.3158
        ],
        [
          "populationTotal",
          0.3171
        ],
        [
          "elevation",
          0.3214
        ]
      ],
      "maj": [
        [
          "populationTotal",
          4.0
        ],
        [
          "minimumElevation",
          2.0
        ],
        [
          "populationDensity",
          1.0
        ]
      ]
    },
    "type": {
      "avg": [
        [
          "http://dbpedia.org/ontology/PopulatedPlace (populationDensity)",
          0.3125
        ],
        [
          "http://dbpedia.org/ontology/Settlement (populationDensity)",
          0.3125
        ],
        [
          "http://dbpedia.org/ontology/Place (populationDensity)",
          0.3125
        ],
        [
          "http://dbpedia.org/ontology/Settlement (minimumElevation)",
          0.315
        ],
        [
          "http://dbpedia.org/ontology/PopulatedPlace (minimumElevation)",
          0.315
        ],
        [
          "http://dbpedia.org/ontology/Location (minimumElevation)",
          0.315
        ],
        [
          "http://dbpedia.org/ontology/Place (minimumElevation)",
          0.315
        ],
        [
          "http://dbpedia.org/ontology/SoccerPlayer (number)",
          0.3158
        ],
        [
          "http://dbpedia.org/ontology/Agent (number)",
          0.3158
        ],
        [
          "http://dbpedia.org/ontology/Person (number)",
          0.3158
        ],
        [
          "http://dbpedia.org/ontology/Athlete (number)",
          0.3158
        ],
        [
          "http://dbpedia.org/ontology/Settlement (populationTotal)",
          0.3163
        ],
        [
          "http://dbpedia.org/ontology/Place (populationTotal)",
          0.3167
        ],
        [
          "http://dbpedia.org/ontology/PopulatedPlace (populationTotal)",
          0.3167
        ],
        [
          "http://dbpedia.org/ontology/Location (populationTotal)",
          0.3171
        ],
        [
          "http://dbpedia.org/ontology/Village (elevation)",
          0.3214
        ],
        [
          "http://dbpedia.org/ontology/Place (elevation)",
          0.3214
        ],
        [
          "http://dbpedia.org/ontology/PopulatedPlace (elevation)",
          0.3214
        ],
        [
          "http://dbpedia.org/ontology/Settlement (elevation)",
          0.3214
        ]
      ],
      "maj": [
        [
          "http://dbpedia.org/ontology/Settlement (populationTotal)",
          9.0
        ],
        [
          "http://dbpedia.org/ontology/Location (populationTotal)",
          9.0
        ],
        [
          "http://dbpedia.org/ontology/SoccerPlayer (number)",
          6.0
        ],
        [
          "http://dbpedia.org/ontology/Settlement (minimumElevation)",
          3.0
        ],
        [
          "http://dbpedia.org/ontology/Location (minimumElevation)",
          3.0
        ],
        [
          "http://dbpedia.org/ontology/Village (elevation)",
          3.0
        ],
        [
          "http://dbpedia.org/ontology/Settlement (populationDensity)",
          3.0
        ],
        [
          "http://dbpedia.org/ontology/Place (populationTotal)",
          2.0
        ],
        [
          "http://dbpedia.org/ontology/Agent (number)",
          2.0
        ],
        [
          "http://dbpedia.org/ontology/PopulatedPlace (populationTotal)",
          2.0
        ],
        [
          "http://dbpedia.org/ontology/Person (number)",
          2.0
        ],
        [
          "http://dbpedia.org/ontology/Athlete (number)",
          2.0
        ],
        [
          "http://dbpedia.org/ontology/PopulatedPlace (populationDensity)",
          1.0
        ],
        [
          "http://dbpedia.org/ontology/PopulatedPlace (minimumElevation)",
          1.0
        ],
        [
          "http://dbpedia.org/ontology/Place (minimumElevation)",
          1.0
        ],
        [
          "http://dbpedia.org/ontology/Place (elevation)",
          1.0
        ],
        [
          "http://dbpedia.org/ontology/PopulatedPlace (elevation)",
          1.0
        ],
        [
          "http://dbpedia.org/ontology/Settlement (elevation)",
          1.0
        ],
        [
          "http://dbpedia.org/ontology/Place (populationDensity)",
          1.0
        ]
      ]
    }
  },
  "neighbours": [
    [
      "Settlement[populationDensity]>(type|Types_of_municipalities_in_Quebec)>(isPartOf|Chaudi%C3%A8re-Appalaches)",
      0.3125
    ],
    [
      "SoccerPlayer[number]>(position|Defender_(association_football))>(birthPlace|Japan)",
      0.313
    ],
    [
      "Location[populationTotal]>(country|Poland)>(type|Human_settlement)>(isPartOf|Pomeranian_Voivodeship)>(22-rdf-syntax-ns#type|_Feature)",
      0.3133
    ],
    [
      "Settlement[populationTotal]>(country|Poland)>(type|Human_settlement)>(isPartOf|Pomeranian_Voivodeship)>(22-rdf-syntax-ns#type|_Feature)",
      0.3133
    ],
    [
      "Location[minimumElevation]>(department|Manche)>(arrondissement|Arrondissement_of_Cherbourg)",
      0.315
    ],
    [
      "Settlement[minimumElevation]>(department|Manche)>(arrondissement|Arrondissement_of_Cherbourg)",
      0.315
    ],
    [
      "SoccerPlayer[number]>(position|Defender_(association_football))>(birthPlace|United_States)",
      0.3185
    ],
    [
      "Settlement[populationTotal]>(country|Canada)>(isPartOf|Saskatchewan)>(type|Hamlet_(place))",
      0.32
    ],
    [
      "Village[elevation]>(isPartOf|Northern_Norway)>(isPartOf|Finnmark)",
      0.3214
    ],
    [
      "Location[populationTotal]>(country|Poland)>(type|Human_settlement)>(isPartOf|Pomeranian_Voivodeship)",
      0.3218
    ]
  ],
  "values": [
    19.39,
    19.39,
    19.41,
    19.37,
    19.38,
    3.06,
    0.02,
    -0.02
  ]
}
'''
