import pydantic as pyd
from typing import List
from consts.permissions import SYSTEM_ADMIN
from consts.roles import ADMIN_ROLE

class TokenData(pyd.BaseModel):
    model_config = pyd.ConfigDict(from_attributes=True, extra='forbid')

    entity_id: int = pyd.Field(
        description = "Identificador único da entidade (usuário)",
        examples =  [20]
    )

    permissions: List[str] = pyd.Field(
        description = "Lista de permissões da entidade (usuário)",
        examples =  []
    )

    role: str | None = pyd.Field(
        description = "Role da entidade (usuário)",
        examples =  ["participant"]
    )


    def has_role(self, role: str) -> bool:
        if not role:
            return False

        if self.role == ADMIN_ROLE:
            return True

        return self.role == role

    def has_permission(self, permission: str) -> bool:
        if len(self.permissions) == 0:
            return False

        if SYSTEM_ADMIN in self.permissions:
            return True

        return permission in self.permissions

    def has_any_permission(self, permissions: List[str]) -> bool:
        if len(self.permissions) == 0:
            return False

        if SYSTEM_ADMIN in self.permissions:
            return True

        for permission in permissions:
            if permission in self.permissions:
                return True

        return False

    def has_all_permission(self, permissions: List[str]) -> bool:
        if len(self.permissions) == 0:
            return False

        if SYSTEM_ADMIN in self.permissions:
            return True

        for permission in permissions:
            if permission not in self.permissions:
                return False

        return True

    def has_owner_id(self, resource_owner_id: int) -> bool:
        if SYSTEM_ADMIN in self.permissions:
            return True

        return resource_owner_id == self.entity_id