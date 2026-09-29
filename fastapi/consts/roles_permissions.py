import consts.permissions as p
import consts.roles as r

ROLE_PERMISSIONS = {
    r.ADMIN_ROLE: [
        p.SYSTEM_ADMIN
    ],
    r.USER_ROLE: [
        p.PREDICT_READ,
        p.PREDICT_CREATE,
        p.PREDICT_UPDATE,
        p.PREDICT_DELETE
    ]
}