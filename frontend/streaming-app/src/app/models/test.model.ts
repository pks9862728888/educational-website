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

  // For unscheduled test
  test_schedule?: number;

  // For other tests
  no_of_optional_section_answer: number;
  question_category: string;
}
