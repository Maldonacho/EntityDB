
import inspect


from typing import Callable, Type

from entitydb.entity import Entity


# Constants
PRIMARY_KEY = "_uid"
ENTITY_TABLE = "_entities"
ENTITY_REFERENCE = "_entity"


class EntityDB():
    '''
    Equivalent to the "world" in ECS terminology.
    Stores entities, can be queried.
    By default has no storage, so cannot function.
    Use the SQLite or Google Cloud Storage versions
    '''

    def __init__(self) -> None:
        self.component_classes: dict[str, type] = dict()
        '''Component classes we have registered'''

    def add_entity(self, entity: Entity) -> int:
        '''
        Adds an entity, returns its ID
        '''
        raise NotImplementedError()

    def new_entity(self, components: list[object]) -> int:
        '''
        Creates a new entity from a list of components.
        Adds it, then returns its ID.
        '''
        return self.add_entity(Entity(components))

    def update_entity(self, entity: Entity) -> bool:
        '''
        Updates the components of an entity that has already been
        saved to the database.
        '''
        raise NotImplementedError()

    def delete_entity(self, entity: Entity) -> bool:
        raise NotImplementedError()

    def run(self, system_func: Callable) -> None:
        '''
        Runs a system, parses the function signature & type hints to know what entities to pass in.

        ## Rules
        - All inputs are required systems by default, unless one of the following applies
        - Make params optional by prefixing name with `opt_*`.
        - Exclude components with: `exclude=[MyExcludedComponent, AnotherComponent]`.
        - Get the entity by adding `entity:Entity` to the params.
        - The EntityDB can be passed in by a param annotated with `EntityDB`. Can be used to create new entities or run more systems.
        - The loop index can be passed in by adding an `int` paramater
        '''
        raise NotImplementedError()

    def count_matches(self, system_func: Callable) -> int:
        '''
        Counts how many entities match the system's signature.
        If you were to run the system, this is how many times it will
        be called.

        TODO some code can be shared with EntityDB.run()
        '''
        raise NotImplementedError()

    def load_component(self, entity: Entity, component_type: type) -> bool:
        '''
        Loads a given component onto an entity, by reading its values from the db.
        If the component already exists on the entity, it is overwritten.

        If this returns True, makes some changes to the given entity:
        - Loads a new component on `Entity._components`
        - Removes the component from `Entity._unloaded_components`, if it was there.
        '''
        raise NotImplementedError()

    def _create_component_from_data(self, component_type: type, component_data: dict) -> object:
        # Just get the actual values, strip the extra stuff
        component_values: dict = {}
        for varname in component_data:
            # Exclude vars that are in the table but not passed into the constructor
            # This should just be the primary key and entity reference
            if varname not in [PRIMARY_KEY, ENTITY_REFERENCE]:
                component_values[varname] = component_data[varname]
        return component_type(**component_values)