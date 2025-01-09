[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/C9zhxHID)
# CS6200 / IS4200: Relevance Judgments

TLDR: In this assignment, you will choose three topics represented in the _Chronicling America_ collection of historic newspapers and record the text of passages relevant to those topics in the file `topics.xml`.

As we discussed in class, the most common way to evaluate ad hoc information retrieval systems is to create *test collections*, as in the [Text Retrieval Conferences (TREC)](https://trec.nist.gov/) run by the US [National Institute of Standards and Technology](https://www.nist.gov/). These consist of a set of information needs, called *topics*. Each topic contains a brief query (the **title**) and longer natural language query (the **description**) and an even longer **narrative** that explains what the user was looking for an what kinds of information count as relevant or not for that information need.

Here is one example TREC topic:

| field | contents |
| ----- | -------- |
| title | pet therapy |
| description | How are pets or animals used in therapy for humans and what are the benefits? |
| narrative | Relevant documents must include details of how pet- or animal-assisted therapy is or has been used. Relevant details include information about pet therapy programs, desscriptions of the circumstances in which pet therapy is used, the benefits of this type of therapy, the degree of success of this therapy, and any laws or regulations governing it. |

After these topics are created, annotators feed the queries to search engines and create *relevance judgments* by looking through the results. The document identifiers of relevant and non-relevant results are appended to each topic.

In this assignment, you will go through the process of creating relevance judgments for an existing set of topics created by the Library of Congress for their [_Chronicling America_](https://www.loc.gov/collections/chronicling-america/about-this-collection/) project, which digitized millions of pages of historic newspapers. As part of this project, librarians have created &ldquo;Research Guides&rdquo; on a few hundred topics. Here is [an alphabetical list of these research guides](https://guides.loc.gov/chronicling-america-topics/alphabetical-order), which you can also view by date, library subject heading, and some other categories.

As an example, consider the research guide for the [bicycle craze in the years around 1900](https://guides.loc.gov/chronicling-america-bicycle-craze). In addition to the narrative and a timeline of events, you can click [&ldquo;Read more about it!&rdquo;](https://guides.loc.gov/chronicling-america-bicycle-craze/selected-articles) to see a list of suggested queries and a few example relevant documents. For most topics, these relevant documents are by no means exhaustive.

**Your task** is to choose **three research guides** and judge the relevance of search results to those topics.  This is made more complex than some evaluations because this is a **passage retrieval** task, i.e., only some of the text on each newspaper page may be relevant to the topic. For instance, [here is the first page listed for the Bicycle Craze topic](https://www.loc.gov/resource/sn85058130/1889-02-24/ed-1/?sp=6&q=bicycles+safety).  Only some of the second column is relevant. Your job, therefore, is to judge whether pages are relevant and, if so, what text on that page is relevant.

You should select relevant passages for at least ten of the documents list on your topics' &ldquo;Read more about it!&rdquo; page&mdash;or for all of them, if there are fewer than ten. In addition, you should judge **five additional** documents by constructing a query and searching *Chronicling America*.  For these five, some of the results may be judged relevant and some non-relevant.  You will record your judgements in a simple XML file.  We have provided the skeleton structure in `topics.xml` for you to edit.  In `bicycle-example.xml`, we show what information you should record:
```xml
<topics>
  <topic>
    <id>https://guides.loc.gov/chronicling-america-bicycle-craze</id>
    <results>
      <result>
	<id>https://www.loc.gov/resource/sn85058130/1889-02-24/ed-1/?sp=6&amp;q=bicycles+safety</id>
	<rel>1</rel>
	<text>THE WORLD ON WHEELS
The Improvements Made The
...
      </text>
      </result>
      <result>
	<id>https://www.loc.gov/resource/sn85058130/1889-03-17/ed-1/?sp=11&amp;q=bicycle+Bicycling+Safeties+safety</id>
	<rel>1</rel>
	<text>ASTRIDE THE WHEEL
Another Plea in Behalf of the
...
      </text>
    </result>
    <result>
      <id>https://www.loc.gov/resource/sn88085722/1891-07-01/ed-1/?sp=2</id>
      <rel>0</rel>
    </result>
  </results>
</topic>
</topics>
```

Each `<topic>` tag should contain an `<id>`, with the URL of the Research Guide, and a `<results>` tag with one or more `<result>` tags.  Each `<result>` contains:
* an `<id>` tag with the URL of the newspaper page,
* a `<rel>` tag containing 1 for relevant or 0 for non-relevant, and
* a `<text>` tag, if the document is relevant, containing the text of the relevant passage.  Relevant passages do not need to contain the query terms, although they may.  If the document is not relevant, you should omit this tag.

To find the text of a newspaper page, click on the &ldquo;Image w/Text&rdquo; link just above the image.  For example, [here is the text of the first result for the Bicycle Craze topic](https://www.loc.gov/resource/sn85058130/1889-02-24/ed-1/?sp=6&q=bicycles+safety&st=text).  (Note that you could also construct this link by appending `&st=text` to the main URL for the newspaper page.) Select the text of the relevant passage and copy it into the `<text>` tag for the result.  Your XML editor may complain about ampersands in the URL. You can replace them with `&amp;` if need be.

Once you have added all this information for three topics to the `topics.xml` file, check in your changes and push them to GitHub.
