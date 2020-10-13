export interface TestMinDetailsResponse {
  question_mode: string;
  question_category: string;
  perm_type: string;
}

export interface TestMinDetailsResponseForQuestionCreation {
  name: string;
  type: string;
  total_marks: number;
  total_duration: number;
  test_schedule_type: string;
  instruction: string;
  test_live: boolean;
  subject_name: string;
  class_name: string;
  test_sets: TestQuestionSet[];
  first_set_questions: SetQuestionsInterface;

  // For unscheduled test
  test_schedule?: number;

  // For other tests
  no_of_optional_section_answer: number;
  question_category: string;
}

export interface TestQuestionSet {
  id: number;
  set_name: string;
  verified: boolean;
  active: boolean;
  mark_as_final: boolean;
  created_on: number;
  delete?: boolean;
}

export interface SetQuestionsInterface {
  // For file type question paper
  id: number;
  file: string;
  delete: boolean;
}
