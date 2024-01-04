# -*- coding: utf-8 -*-

from knext.client.model.builder_job import BuilderJob
from knext.api.component import CSVReader, SPGTypeMapping, KGWriter

from schema.test_schema_helper import TEST


class Test(BuilderJob):
    def build(self):
        source = CSVReader(
            local_path="./builder/job/data/data.csv",
            columns=[
                "id",
                "text",
                "integer",
                "float",
                "standard",
                "concept",
                "confidence_concept",
                "lead_to_concept2",
                "lead_to_concept3" "event",
                "confidence_event",
                "source_event",
                "entity",
                "entity_relation",
            ],
            start_row=1,
        )

        event_mapping = (
            SPGTypeMapping(spg_type_name=TEST.CenterEvent)
            .add_property_mapping("id", TEST.CenterEvent.id)
            .add_property_mapping("id", TEST.CenterEvent.name)
            .add_property_mapping("text", TEST.CenterEvent.basicTextProperty)
            .add_property_mapping("integer", TEST.CenterEvent.basicIntegerProperty)
            .add_property_mapping("float", TEST.CenterEvent.basicFloatProperty)
            .add_property_mapping("standard", TEST.CenterEvent.standardProperty)
            .add_property_mapping(
                "concept", TEST.CenterEvent.conceptProperty, TEST.Concept1
            )
            .add_sub_property_mapping("confidence_concept", "confidence")
            .add_property_mapping("entity", TEST.CenterEvent.subject, TEST.Entity1)
            .add_relation_mapping(
                "event", TEST.CenterEvent.eventRelation, TEST.CenterEvent
            )
            .add_sub_property_mapping("confidence_event", "confidence")
            .add_sub_property_mapping("source_event", "source")
        )

        entity_mapping = (
            SPGTypeMapping(spg_type_name=TEST.Entity1)
            .add_property_mapping("entity", TEST.Entity1.id)
            .add_property_mapping("entity", TEST.Entity1.name)
            .add_relation_mapping(
                "entity_relation", TEST.Entity1.entityRelation, TEST.Entity2
            )
            .add_predicting_relation(TEST.Entity1.predictRelation, TEST.Entity3)
        )

        concept_mapping = (
            SPGTypeMapping(spg_type_name=TEST.Concept1)
            .add_property_mapping("concept", TEST.Concept1.id)
            .add_property_mapping("concept", TEST.Concept1.name)
            .add_relation_mapping(
                "lead_to_concept2", TEST.Concept1.leadTo, TEST.Concept2
            )
            .add_relation_mapping(
                "lead_to_concept3", TEST.Concept1.leadTo, TEST.Concept3
            )
        )

        sink = KGWriter()

        return source >> [event_mapping, entity_mapping, concept_mapping] >> sink
