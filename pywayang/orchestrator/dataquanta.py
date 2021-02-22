from orchestrator.operator import Operator


class DataQuantaBuilder:
    def __init__(self, descriptor):
        self.descriptor = descriptor

    def source(self, source):

        # Uncomment to execute directly without Wayang
        if type(source) is str:
            source_ori = open(source, "r")
        else:
            source_ori = source
        return DataQuanta(
            Operator(
                operator_type="source",
                udf=source,
                iterator=iter(source_ori),
                wrapper="URL"
            ),
            descriptor=self.descriptor
        )


class DataQuanta:
    def __init__(self, operator=None, descriptor=None):
        self.operator = operator
        self.descriptor = descriptor
        if self.operator.is_source():
            self.descriptor.add_source(self.operator)
        if self.operator.is_sink():
            self.descriptor.add_sink(self.operator)

    # Operational Functions
    def filter(self, udf):
        def func(iterator):
            return filter(udf, iterator)

        return DataQuanta(
            Operator(
                operator_type="filter",
                udf=func,
                previous=self.operator,
                wrapper="predicate"
            ),
            descriptor=self.descriptor
        )

    def map(self, udf):
        def func(iterator):
            return map(udf, iterator)

        return DataQuanta(
            Operator(
                operator_type="map",
                udf=func,
                previous=self.operator,
                wrapper="transform"
            ),
            descriptor=self.descriptor
        )

    def sink(self, path, end="\n"):
        def consume(iterator):
            with open(path, 'w') as f:
                for x in iterator:
                    f.write(str(x) + end)

        def func(iterator):
            consume(iterator)
            # return self.__run(consume)

        return DataQuanta(
            Operator(
                operator_type="sink",

                udf=path,
                # To execute directly uncomment
                #udf=func,

                previous=self.operator,
                wrapper="URL,end"
            ),
            descriptor=self.descriptor
        )

    def sort(self, udf):

        def func(iterator):
            return sorted(iterator, key=udf)

        return DataQuanta(
            Operator(
                operator_type="sort",
                udf=func,
                previous=self.operator,
                wrapper="wrapped_python"
            ),
            descriptor=self.descriptor
        )

    def __run(self, consumer):
        consumer(self.operator.getIterator())

    # Execution Functions
    def console(self, end="\n"):
        def consume(iterator):
            for x in iterator:
                print(x, end=end)

        self.__run(consume)

    def execute(self):
        # print(self.operator.previous[0].operator_type)
        if self.operator.is_sink():
            self.operator.udf(self.operator.previous[0].getIterator())
        else:
            print("Plan must call execute from SINK type of operator")
            raise RuntimeError
