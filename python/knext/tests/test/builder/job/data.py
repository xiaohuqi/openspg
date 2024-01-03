# -*- coding: utf-8 -*-

from knext.client.model.builder_job import BuilderJob
from knext.api.component import CSVReader, SPGTypeMapping, KGWriter

try:
    from schema.test_schema_helper import TEST
except:
    pass


class Data(BuilderJob):

    def build(self):
        source = CSVReader(
            local_path="./builder/job/data/data.csv",
            columns=["id", "text", "integer", "float", "standard", "concept", "lead_to_concept", "relevant_event_id", "subject_entity_id", "subject_relation_id"],
            start_row=1
        )

        event_mapping = (
            SPGTypeMapping(spg_type_name=TEST.CenterEvent)
            .add_mapping_field("id", TEST.CenterEvent.id)
            .add_mapping_field("name", TEST.CenterEvent.name)
            .add_mapping_field("text", TEST.CenterEvent.basicTextProperty)
            .add_mapping_field("integer", TEST.CenterEvent.basicIntegerProperty)
            .add_mapping_field("float", TEST.CenterEvent.basicFloatProperty)
            .add_mapping_field("event", TEST.CenterEvent.eventProperty)
            .add_mapping_field("entity", TEST.CenterEvent.subject)
            .add_mapping_field("standard", TEST.CenterEvent.standardProperty)
            .add_mapping_field("concept", TEST.CenterEvent.conceptProperty)
            .add_mapping_field("relation", TEST.CenterEvent.entityRelation, TEST.Entity2)
        )

        entity_mapping = (
            SPGTypeMapping(spg_type_name=TEST.Entity1)
            .add_mapping_field("id", TEST.Entity1.id)
            .add_mapping_field("name", TEST.Entity1.name)
            .add_mapping_field("entity", TEST.Entity1.entityProperty)
            .add_predicting_field(TEST.Entity1.predictProperty)
        )

        concept_mapping = (
            SPGTypeMapping(spg_type_name=TEST.Concept1)
            .add_mapping_field("id", TEST.Concept1.id)
            .add_mapping_field("name", TEST.Concept1.name)
            .add_mapping_field("leadTo", TEST.Concept1.leadTo, TEST.Concept2)
        )

        sink = KGWriter()

        return source >> extract >> [event_mapping, entity_mapping, concept_mapping] >> sink
