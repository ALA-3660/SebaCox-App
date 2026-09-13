/// Demand Repository interfacing with Service layer.
/// "প্রয়োজন থেকে সমাধান- এক অ্যাপেই"
library;

import '../models/demand_model.dart';
import '../services/demand_service.dart';

class DemandRepository {
  final DemandApiService _apiService;

  DemandRepository({required DemandApiService apiService}) : _apiService = apiService;

  Future<List<DemandModel>> fetchDemands({
    String? query,
    int? serviceId,
    int? categoryId,
    int? upazilaId,
    String? token,
  }) => _apiService.getDemands(
    query: query,
    serviceId: serviceId,
    categoryId: categoryId,
    upazilaId: upazilaId,
    token: token,
  );

  Future<List<DemandModel>> fetchMyDemands(String token) => _apiService.getMyDemands(token: token);

  Future<DemandModel> createDemand({
    required String token,
    required Map<String, dynamic> data,
    bool publishNow = false,
  }) => _apiService.createDemand(token: token, data: data, publishNow: publishNow);

  Future<DemandModel> publishDemand(String token, int demandId) =>
      _apiService.performLifecycleAction(token: token, demandId: demandId, action: 'publish');

  Future<DemandModel> pauseDemand(String token, int demandId, {String reason = ''}) =>
      _apiService.performLifecycleAction(token: token, demandId: demandId, action: 'pause', body: {'reason': reason});

  Future<DemandModel> resumeDemand(String token, int demandId) =>
      _apiService.performLifecycleAction(token: token, demandId: demandId, action: 'resume');

  Future<DemandModel> cancelDemand(String token, int demandId, {String reason = ''}) =>
      _apiService.performLifecycleAction(token: token, demandId: demandId, action: 'cancel', body: {'reason': reason});

  Future<DemandModel> fulfillDemand(String token, int demandId, {String note = ''}) =>
      _apiService.performLifecycleAction(token: token, demandId: demandId, action: 'fulfill', body: {'note': note});

  Future<DemandModel> closeDemand(String token, int demandId, {String reason = ''}) =>
      _apiService.performLifecycleAction(token: token, demandId: demandId, action: 'close', body: {'reason': reason});
}
