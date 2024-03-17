from typing import List
from lib.core.entity.models import KnowledgeSourceEnum, SourceData
from lib.core.ports.primary.list_source_data_for_research_context_primary_ports import (
    ListSourceDataForResearchContextOutputPort,
)
from lib.core.usecase_models.list_source_data_for_research_context_usecase_models import (
    ListSourceDataForResearchContextError,
    ListSourceDataForResearchContextResponse,
)
from lib.core.view_model.list_source_data_for_research_context_view_model import (
    ListSourceDataForResearchContextViewModel,
    MPIScraperLFNViewModel,
)


class ListSourceDataForResearchContextPresenter(ListSourceDataForResearchContextOutputPort):
    def _MPI_pfn_to_lfn(
        self, pfn: str, self_host: str, self_port: int, self_bucket: str, self_protocol: str, source_data_id: int
    ) -> MPIScraperLFNViewModel:
        """
        Generate a LFN from a PFN for MinIO S3 Repository.

        :param pfn: The PFN to generate a LFN for.
        :type pfn: str
        :raises ValueError: If the PFN protocol is S3.
        :return: The LFN.
        """
        self_url = f"{self_host}:{self_port}"

        if pfn.startswith(f"{self_protocol}://{self_host}:{self_port}/{self_bucket}"):
            without_protocol = pfn.split("://")[1]
            path_components = without_protocol.split("/")[1:]
            bucket = path_components[0]

            if bucket != self_bucket:
                raise ValueError(
                    f"Bucket {bucket} does not match the bucket of this MinIO Repository at {self_url}. Cannot create a LFN for PFN {pfn}."
                )
            tracer_key = path_components[1]
            source = KnowledgeSourceEnum(path_components[2])
            job_id = int(path_components[3])
            relative_path = "/".join(path_components[4:])

            lfn: MPIScraperLFNViewModel = MPIScraperLFNViewModel(
                source_data_id=source_data_id,
                source_data_lfn=pfn,
                protocol=self_protocol,
                tracer_key=tracer_key,
                source=str(source.value),
                job_id=job_id,
                relative_path=relative_path,
            )

            return lfn

        raise ValueError(
            f"Path {pfn} is not supported by this MinIO Repository at {self_url}. Cannot create a LFN for PFN {pfn}."
        )

    def convert_error_response_to_view_model(
        self, response: ListSourceDataForResearchContextError
    ) -> ListSourceDataForResearchContextViewModel:
        return ListSourceDataForResearchContextViewModel(
            status=False,
            lfn_list=[],
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )

    def convert_response_to_view_model(
        self, response: ListSourceDataForResearchContextResponse
    ) -> ListSourceDataForResearchContextViewModel:
        source_data_list: List[SourceData] = response.source_data_list

        lfn_vm_list: List[MPIScraperLFNViewModel] = []

        for sd in source_data_list:
            pfn = sd.lfn
            without_protocol = pfn.split("://")[1]
            path_components = without_protocol.split("/")
            url = path_components[0]
            host = url.split(":")[0]
            port = int(url.split(":")[1])
            bucket = path_components[1]
            sd_protocol_value = sd.protocol.value

            lfn_vm = self._MPI_pfn_to_lfn(
                pfn=sd.lfn,
                self_host=host,
                self_port=port,
                self_bucket=bucket,
                self_protocol=sd_protocol_value,
                source_data_id=sd.id,
            )

            lfn_vm_list.append(lfn_vm)

        lfn_list = [lfn_vm.model_dump_json() for lfn_vm in lfn_vm_list]

        return ListSourceDataForResearchContextViewModel(
            status=True,
            code=200,
            lfn_list=lfn_list,
        )
