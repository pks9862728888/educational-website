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
  first_set_questions: FileQuestionsInterface;

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
  first_set_questions: ImageQuestionsSectionInterface[];
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
  edit?: boolean;
  editingIndicator?: boolean;
  showAddSectionForm?: boolean;
}

export interface FileQuestionsInterface {
  id: number;
  file: string;
  delete?: boolean;
}

export interface ImageQuestionsSectionInterface {
  section_id: number;
  name?: string;
  order: number;
  view: string;
  no_of_question_to_attempt: number;
  answer_all_questions: boolean;
  section_mandatory: boolean;
  questions: SubjectImageTestQuestions[];
  edit?: boolean;
  editingIndicator?: boolean;
  deletingIndicator?: boolean;
}

export interface SubjectImageTestQuestions {
  question_id: number;
  marks: number;
  order: number;
  text: string;
  file: string;
  concept_label_id: number;
  delete?: boolean;
  edit?: boolean;
  removingLabelIndicator?: boolean;
}

export interface SubjectTestSection {
  id: number;
  name: string;
  view: string;
  section_mandatory: boolean;
  answer_all_questions: boolean;
  no_of_question_to_attempt?: number;
}


export interface TestMinDetailsResponseForTypedTestQuestionCreation {
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
  first_set_questions: TypedQuestionsSectionInterface[];
  labels?: TestConceptLabelInterface[];

  // For unscheduled test
  test_schedule?: number;

  // For other tests
  no_of_optional_section_answer: number;
  question_category: string;
}


export interface TypedQuestionsSectionInterface {
  section_id: number;
  name?: string;
  order: number;
  view: string;
  no_of_question_to_attempt: number;
  answer_all_questions: boolean;
  section_mandatory: boolean;
  questions: SubjectTypedTestQuestions[];
  edit?: boolean;
  editingIndicator?: boolean;
  deletingIndicator?: boolean;
}

export interface SubjectTypedTestQuestions {
  question_id: number;
  marks: number;
  order: number;
  question: string;
  type: string;
  has_image: boolean;
  concept_label_id: number;

  correct_answer?: string | boolean | number;

  delete?: boolean;
  edit?: boolean;
  removingLabelIndicator?: boolean;
  showAddAnswerForm?: boolean;
  showAddAnswerIndicator?: boolean;
}
