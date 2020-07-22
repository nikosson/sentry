import React from 'react';

import AsyncComponent from 'app/components/asyncComponent';
import AvatarList from 'app/components/avatar/avatarList';
import {Organization, Team} from 'app/types';

type Props = AsyncComponent['props'] & {
  teamId: Team['id'];
  orgId: Organization['id'];
};

type State = AsyncComponent['state'];

class TeamMembers extends AsyncComponent<Props, State> {
  getEndpoints(): ReturnType<AsyncComponent['getEndpoints']> {
    const {orgId, teamId} = this.props;
    return [['members', `/teams/${orgId}/${teamId}/members/`]];
  }

  renderBody() {
    const {members} = this.state;

    console.log('members', members);

    if (!members) {
      return null;
    }

    const users = members.filter(({user}) => !!user).map(({user}) => user);
    return <AvatarList users={users} />;
  }
}

export default TeamMembers;
