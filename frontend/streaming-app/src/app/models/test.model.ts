export interface TestMinDetailsResponse {
  question_mode: string;
  question_category: string;
  perm_type: string;
}

export interface TestMinDetailsResponseForFileTestQuestionCreation {
  name: string;
  type: string;
  total_marks: number;
  total_duration: number;
  test_schedule_type: string;
  instruction: string;
  test_live: boolean;
  subject_name: string;
  class_name: string;
  test_sets: TestQuestionSetInterface[];
  first_set_questions: SetFileQuestionsInterface;

  // For unscheduled test
  test_schedule?: number;

  // For other tests
  no_of_optional_section_answer: number;
  question_category: string;
}

export interface TestMinDetailsResponseForImageTestQuestionCreation {
  name: string;
  type: string;
  total_marks: number;
  total_duration: number;
  test_schedule_type: string;
  instruction: string;
  test_live: boolean;
  subject_name: string;
  class_name: string;
  test_sets: TestQuestionSetInterface[];
  first_set_questions: SetImageQuestionsInterface;
  labels?: TestConceptLabelInterface[];

  // For unscheduled test
  test_schedule?: number;

  // For other tests
  no_of_optional_section_answer: number;
  question_category: string;
}

export interface TestConceptLabelInterface {
  id: number;
  name: string;
}

export interface TestQuestionSetInterface {
  id: number;
  set_name: string;
  verified: boolean;
  active: boolean;
  mark_as_final: boolean;
  created_on: number;
  delete?: boolean;
}

export interface SetFileQuestionsInterface {
  id: number;
  file: string;
  delete?: boolean;
}

export interface SetImageQuestionsInterface {
  id: number;
  test_section: SubjectTestSection;
  file: string;
  marks: number;
  delete: boolean;
}

export interface SubjectTestSection {
  id: number;
  name: string;
  view: string;
  section_mandatory: boolean;
  answer_all_questions: boolean;
  no_of_question_to_attempt?: number;
}
