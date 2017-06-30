from __future__ import print_function, absolute_import
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText

import logging

logging.basicConfig(level=logging.INFO)


class FindWords(beam.DoFn):
    def process(self, element):
        import re as regex
        return regex.findall(r"[A-Za-z\']+", element)


class CountWordsTransform(beam.PTransform):
    def expand(self, p_collection):
        # p_collection is collection of loaded lines
        return (p_collection
                | "Split" >> (beam.ParDo(FindWords()).with_input_types(unicode))
                | "PairWithOne" >> beam.Map(lambda word: (word, 1))
                | "GroupBy" >> beam.GroupByKey()
                | "AggregateGroups" >> beam.Map(lambda (word, ones): (word, sum(ones))))


def run():
    import time
    gcs_path = "gs://marcin-playground/dataflow"
    pipeline =  beam.Pipeline(runner="DataflowRunner", argv=[
        "--project", "project-name",
        "--staging_location", ("%s/staging_location" % gcs_path),
        "--temp_location", ("%s/temp" % gcs_path),
        "--output", ("%s/output" % gcs_path),
        "--setup_file", "./setup.py"
    ])
    (pipeline
     | "Load" >> ReadFromText("gs://marcin-playground/books/*.txt")
     | "Count Words" >> CountWordsTransform()
     | "FormatOutput" >> beam.Map(lambda (word, count): "{0}: {1}".format(word, count))
     | "Save" >> WriteToText("{0}/output/wordcount{1}".format(gcs_path, int(time.time())))
     )
    pipeline.run()
