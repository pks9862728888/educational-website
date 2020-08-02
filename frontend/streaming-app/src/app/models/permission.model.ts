export interface BaseInvitation {
  email: string;
  image: string;
  invitation_id: number;
  invitee_id: number;
  inviter: string;
}

export interface UserActiveInviteMinDetails extends BaseInvitation {
  request_accepted_on: string;
}

export interface UserPendingInviteMinDetails extends BaseInvitation{
  requested_on: string;
}

export interface InstituteAdminListResponse {
  active_admin_list: UserActiveInviteMinDetails[];
  pending_admin_invites: UserPendingInviteMinDetails[];
}

export interface InstituteStaffListResponse {
  active_staff_list: UserActiveInviteMinDetails[];
  pending_staff_invites: UserPendingInviteMinDetails[];
}

export interface InstituteFacultyListResponse {
  active_faculty_list: UserActiveInviteMinDetails[];
  pending_faculty_invites: UserPendingInviteMinDetails[];
}
