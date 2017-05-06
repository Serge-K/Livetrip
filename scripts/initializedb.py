import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from models.meta import Base
import models

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = models.get_engine(settings)

    try:
        print("Drop all tables")
        Base.metadata.drop_all(engine)
    except:
        pass

    print("Create all tables")
    Base.metadata.create_all(engine)

    session_factory = models.get_session_factory(engine)

    print("Initialize DB init params")
    with transaction.manager:
        dbsession = models.get_tm_session(session_factory, transaction.manager)

        """ Init admin user and permission """
        admin_group = AdminGroup('Admin')
        admin_group.description = 'Администратор'
        dbsession.add(admin_group)
        dbsession.flush()

        for perm in ('read', 'write', 'delete', 'create', 'disabled'):
            admin_perm = AdminPermission(perm)
            admin_perm.groups.append(admin_group)
            dbsession.add(admin_perm)
            dbsession.flush()

        admin_user = AdminUser('GAdmin', 'admin@admin.com', '123456')
        admin_user.groups.append(admin_group)
        dbsession.add(admin_user)
        dbsession.flush()

        setting_group = AppSettingGroup(name="Без группы")
        dbsession.add(setting_group)
        dbsession.flush()
