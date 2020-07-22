import React from 'react';
import styled from '@emotion/styled';

import space from 'app/styles/space';
import {Team, Organization} from 'app/types';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import DateTime from 'app/components/dateTime';

import TeamMembers from './teamMembers';

type Props = {
  team: Team;
  organization: Organization;
  hasTeamAdminAccess: boolean;
};

const TeamCard = ({hasTeamAdminAccess, organization, team}: Props) => {
  return (
    <Wrapper>
      <Header>
        {hasTeamAdminAccess ? (
          <TeamLink to={`/settings/${organization.slug}/teams/${team.slug}/`}>
            <IdBadge team={team} avatarSize={22} />
          </TeamLink>
        ) : (
          <IdBadge team={team} avatarSize={22} />
        )}
      </Header>
      <Body>
        <Description>
          {
            'Curabitur ligula sapien, tincidunt non, euismod vitae, posuere imperdiet, leo. Maecenas malesuada. Praesent congue erat at massa.'
          }
        </Description>
        <TeamMembers orgId={organization.id} teamId={team.id} />
        <div>
          <DateTime date={team.dateCreated} />
        </div>
      </Body>
    </Wrapper>
  );
};

export default TeamCard;

const Wrapper = styled('div')`
  background-color: ${p => p.theme.white};
  border: 1px solid ${p => p.theme.gray400};
  border-radius: ${p => p.theme.borderRadius};
  box-shadow: ${p => p.theme.dropShadowLight};
  padding: ${space(1)};
  display: grid;
  grid-gap: ${space(1)};
`;

const Header = styled('div')``;
const Body = styled('div')`
  display: grid;
  grid-gap: ${space(1)};
`;
const Description = styled('div')`
  color: ${p => p.theme.gray500};
  font-size: ${p => p.theme.fontSizeMedium};
`;

const TeamLink = styled(Link)`
  display: flex;
  align-items: center;
`;
