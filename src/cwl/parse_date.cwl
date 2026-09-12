#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: ExpressionTool

requirements:
  InlineJavascriptRequirement: {}


inputs:
  date:
    type: string

outputs:
  year:
    type: string
  month:
    type: string
  day:
    type: string

expression: |
  ${
    const parts = inputs.date.split('-');
    return {
      year: parts[0],
      month: parts[1],
      day: parts[2]
    };
  }