from seoanalyzer import analyze
from pprint import pprint


url = "http://www.emergencyrooter.com/"

def seo_analyze(url):
  info = analyze(url, analyze_headings=True, analyze_extra_tags=True, follow_links=False)
  p = info['pages'][0]

  title = p['title'].capitalize()

  description = p['description'].capitalize()

  headings = p['headings']
  h_tags = find_headings(headings)

  keywords = p['keywords'][:5]
  keyword_results = get_keywords(keywords)

  warnings = p['warnings'][:-1]
  warning_results = warning_check(warnings)

  wordcount = p['word_count']

  seo_data = {"website_title": title,
              "website_description": description,
              "h_tags": h_tags,
              "keyword_results": keyword_results,
              "warning_results": warning_results,
              "wordcount": wordcount}

  # flatten_dictionary(seo_data)
  return seo_data


def find_headings(headings):

  h_tags = {}

  for k,v in headings.items():
    h_tags[k] = {}
    h_tags[k]['data'] = {}
    h_tags[k]['content'] = f"Your homepage has {len(v)} {k} tags."
    for i in range(len(v)):
      h_tags[k]['data'][str(i+1)] = v[i]

  return h_tags

def get_keywords(keywords):

  k_words = {}

  num = 1
  for i in keywords:
    k_words[i[1]] = {}
    k_words[i[1]]['count'] = i[0]
    k_words[i[1]]['content'] = f"'{i[1]}' appeared {i[0]} times."
    num += 1

  return k_words

def warning_check(warnings):

  warning_codes = {}
  total_warning_codes = 0
  warning_codes['data'] = {}

  for i in warnings:
    warning = i.split(":")
    wType = warning[0]
    if wType not in warning_codes['data']:
      warning_codes['data'][wType] = 0
    warning_codes['data'][wType] += 1
    total_warning_codes += 1

  count = 1
  for k,v in warning_codes['data'].items():
    warning_codes['data'][k] = v
    count+=1

  warning_codes['content'] = f"Your website has {total_warning_codes} total warning codes that need to be fixed."
  return warning_codes

def flatten_dictionary(dictionary):
    # print(dictionary)
    def recursor(parentK, givenVal):
        if type(givenVal) != dict:
            o[parentK] = givenVal
            return
        else:
            for eachChildK in givenVal.keys():
                if eachChildK == "":
                    recursor(parentK, givenVal[eachChildK])
                else:
                    if parentK != "":
                        recursor(parentK + "." + eachChildK, givenVal[eachChildK])
                    else:
                        recursor(eachChildK, givenVal[eachChildK])

    o = {}
    for eachK in dictionary.keys():
        recursor(eachK, dictionary[eachK])

    # restruct_data(o)
    return o


def restruct_data(flatD):
    title = ""
    description = ""
    headings = ""
    keywords = ""
    warnings = ""
    wordcount = ""


    for k, v in flatD.items():
        if "website_title" in k:
            title += v.strip() + " "

        elif "website_description" in k:
            description += str(v).strip() + " "

        elif "h_tags" in k and "content" in k:
            headings += f"\n\n{str(v).strip()} "

        elif "h_tags" in k and "data" in k:
            headings += f"\n - {str(v).strip()}"

        elif "keyword" in k and "content" in k:
            keywords += f"- {str(v).strip()}\n"

        elif "warning" in k and "content" in k:
            warnings += str(v).strip() + " "

        elif "wordcount" in k:
            wordcount += str(v).strip() + " "

    structured_content = {
        'title': title,
        'description': description,
        'headings': headings,
        'keywords': keywords,
        'warnings': warnings,
        'wordcount': wordcount
    }
    return structured_content

#
# url = 'http://dominguezfirm.com'
#
# analysis = seo_analyze(url)
# flat_analysis = flatten_dictionary(analysis)
# restruct_analysis = restruct_data(flat_analysis)



